#!/usr/bin/env python3
"""
Scraper especializado para datos de Boxscore de NBA
"""

import logging
import time
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import polars as pl
from django.db import transaction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from data.models import BoxScore
from scrapper.models import ScrapperLogs
from source.models import Links

from .base_scrapper import BaseScraper

logger = logging.getLogger(__name__)


class BoxscoreScraper(BaseScraper):
    """
    Scraper especializado para datos de Boxscore
    """

    def get_table_selector(self):
        """
        Selector específico para la tabla de Boxscore
        """
        return "table.Crom_table__p1iZz"

    def get_next_page_button_selector(self):
        """
        Selector CSS para el botón de página siguiente

        Returns:
            str: Selector CSS del botón de siguiente página
        """
        # Selector común para el botón de siguiente página en NBA Stats
        # Ajusta este selector según la estructura real de la página
        return "button[aria-label='Next Page'], .Pagination_content_f2at7 button:last-child, [data-cy='next-page-button']"

    def _has_next_page(self):
        """
        Verifica si hay una página siguiente disponible

        Returns:
            bool: True si hay una página siguiente
        """
        try:
            next_button = self.driver.find_element(
                By.CSS_SELECTOR, self.get_next_page_button_selector()
            )
            # Verificar si el botón está habilitado (no tiene atributo disabled)
            is_enabled = next_button.is_enabled()
            # Verificar si no tiene la clase disabled
            classes = next_button.get_attribute("class") or ""
            is_disabled = "disabled" in classes.lower() or "inactive" in classes.lower()
            return is_enabled and not is_disabled
        except NoSuchElementException:
            return False
        except Exception as e:
            logger.warning(f"Error verificando siguiente página: {e}")
            return False

    def _click_next_page(self):
        """
        Hace clic en el botón de página siguiente

        Returns:
            bool: True si el clic fue exitoso
        """
        try:
            next_button = self.driver.find_element(
                By.CSS_SELECTOR, self.get_next_page_button_selector()
            )

            # Desplazarse al botón si es necesario
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", next_button
            )
            time.sleep(0.5)

            # Intentar hacer clic con JavaScript si el clic normal falla
            try:
                next_button.click()
            except:
                self.driver.execute_script("arguments[0].click();", next_button)

            # Esperar a que la nueva página cargue
            time.sleep(2)

            # Esperar a que la tabla esté presente en la nueva página
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.get_table_selector())
                )
            )

            logger.info("Navegado a la página siguiente")
            return True
        except NoSuchElementException:
            logger.warning("No se encontró el botón de página siguiente")
            return False
        except Exception as e:
            logger.error(f"Error haciendo clic en siguiente página: {e}")
            return False

    def extract_data(self, url):
        """
        Extrae datos específicos de Boxscore con soporte para paginación

        Args:
            url (str): URL actual

        Returns:
            pl.DataFrame: Datos extraídos de todas las páginas
        """
        all_dataframes = []
        page_number = 1

        try:
            while True:
                logger.info(f"Extrayendo datos de la página {page_number}")

                # Buscar la tabla de datos
                table = self.driver.find_element(
                    By.CSS_SELECTOR, self.get_table_selector()
                )

                # Extraer encabezados
                headers = []
                header_row = table.find_element(By.TAG_NAME, "thead")
                header_cells = header_row.find_elements(By.TAG_NAME, "th")

                for cell in header_cells:
                    headers.append(cell.text.strip())

                # Extraer filas de datos
                rows = []
                game_ids = []  # Guardar game_ids por separado
                tbody = table.find_element(By.TAG_NAME, "tbody")
                data_rows = tbody.find_elements(By.TAG_NAME, "tr")

                for row in data_rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    row_data = []
                    game_id = None

                    for cell in cells:
                        # Manejar celdas que pueden contener enlaces
                        # Extraer el texto del enlace si existe, sino el texto de la celda
                        try:
                            link = cell.find_element(By.TAG_NAME, "a")
                            cell_text = link.text.strip()

                            # Si el href contiene "/game/", extraer el game_id
                            href = link.get_attribute("href")
                            if href and "/game/" in href:
                                # Extraer el ID del juego del href
                                # Ejemplos:
                                # /game/0022500140 -> 0022500140
                                # https://www.nba.com/game/0022500140 -> 0022500140
                                parts = href.split("/game/")
                                if len(parts) > 1:
                                    game_id = (
                                        parts[-1].split("/")[0].split("?")[0].strip()
                                    )
                        except NoSuchElementException:
                            cell_text = cell.text.strip()

                        row_data.append(cell_text)

                    if row_data:  # Solo agregar filas con datos
                        rows.append(row_data)
                        game_ids.append(game_id if game_id else None)

                # Crear DataFrame para esta página
                if rows and headers:
                    df = pl.DataFrame(rows, columns=headers)

                    # Agregar columna game_id si se encontró algún game_id
                    if any(game_ids):
                        df = df.with_columns(pl.Series("game_id", game_ids))

                    # Agregar metadatos
                    df = df.with_columns(pl.lit(url).alias("source_url"))
                    df = df.with_columns(pl.lit("boxscore").alias("category"))
                    df = df.with_columns(pl.lit(page_number).alias("page_number"))

                    # Limpiar datos
                    df = self._clean_data(df)

                    all_dataframes.append(df)
                    logger.info(
                        f"Extraídos {len(df)} registros de la página {page_number}"
                    )

                # Verificar si hay una página siguiente
                if not self._has_next_page():
                    logger.info("No hay más páginas disponibles")
                    break

                # Intentar navegar a la página siguiente
                if not self._click_next_page():
                    logger.warning("No se pudo navegar a la página siguiente")
                    break

                page_number += 1

                # Limite de seguridad para evitar bucles infinitos
                if page_number > 1000:
                    logger.warning("Límite de páginas alcanzado (1000)")
                    break

            # Combinar todos los DataFrames
            if all_dataframes:
                combined_df = pl.concat(all_dataframes)
                logger.info(
                    f"Total de registros extraídos: {len(combined_df)} de {page_number} página(s)"
                )
                return combined_df
            else:
                return pl.DataFrame()

        except Exception as e:
            logger.error(f"Error extrayendo datos de Boxscore: {e}")

            # Si hay datos parciales, devolverlos
            if all_dataframes:
                return pl.concat(all_dataframes)
            return pl.DataFrame()

    def _clean_data(self, df):
        """
        Limpia y procesa los datos específicos de Boxscore

        Args:
            df (pl.DataFrame): DataFrame a limpiar

        Returns:
            pl.DataFrame: DataFrame limpio
        """
        try:
            # Convertir columnas numéricas (usando nombres reales del HTML)
            numeric_columns = [
                "MIN",
                "PTS",
                "FGM",
                "FGA",
                "FG%",
                "3PM",
                "3PA",
                "3P%",
                "FTM",
                "FTA",
                "FT%",
                "OREB",
                "DREB",
                "REB",
                "AST",
                "STL",
                "BLK",
                "TOV",
                "PF",
                "PLUS_MINUS",
            ]

            for col in numeric_columns:
                if col in df.columns:
                    # Intentar convertir a Float64, si falla mantener como string
                    try:
                        df = df.with_columns(
                            pl.col(col)
                            .str.replace_all("%", "")
                            .cast(pl.Float64, strict=False)
                            .alias(col)
                        )
                    except:
                        try:
                            df = df.with_columns(
                                pl.col(col).cast(pl.Float64, strict=False).alias(col)
                            )
                        except:
                            # Si no se puede convertir, dejar como está
                            pass

            # Limpiar nombres de equipos (puede ser "Team" o "TEAM")
            team_cols = ["Team", "TEAM"]
            for col in team_cols:
                if col in df.columns:
                    df = df.with_columns(pl.col(col).str.strip_chars().alias(col))

            # Limpiar fechas (puede ser "Game Date" o similar)
            date_cols = ["Game Date", "GDATE"]
            for col in date_cols:
                if col in df.columns:
                    df = df.with_columns(pl.col(col).str.strip_chars().alias(col))

            # Agregar timestamp
            df = df.with_columns(pl.lit(pl.datetime.now()).alias("scraped_at"))

            return df

        except Exception as e:
            logger.error(f"Error limpiando datos: {e}")
            return df

    def _extract_url_params(self, url):
        """
        Extrae season y season_type de la URL

        Args:
            url (str): URL a analizar

        Returns:
            tuple: (season, season_type)
        """
        try:
            parsed = urlparse(url)
            qs = parse_qs(parsed.query)
            season_type = qs.get("SeasonType", [""])[0].replace("+", " ")
            season = qs.get("Season", [""])[0]
            return season, season_type
        except Exception as e:
            logger.warning(f"Error extrayendo parámetros de URL: {e}")
            return None, None

    def _parse_game_date(self, date_str):
        """
        Parsea una fecha de string a objeto date

        Args:
            date_str (str): Fecha en formato string

        Returns:
            date: Objeto date o None si no se puede parsear
        """
        if not date_str:
            return None

        # Diferentes formatos posibles
        date_formats = ["%m/%d/%Y", "%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"]

        for fmt in date_formats:
            try:
                return datetime.strptime(str(date_str).strip(), fmt).date()
            except (ValueError, AttributeError):
                continue

        logger.warning(f"No se pudo parsear la fecha: {date_str}")
        return None

    def _map_dataframe_to_model(self, df, season, season_type, url):
        """
        Mapea un DataFrame de Polars a objetos BoxScore

        Args:
            df (pl.DataFrame): DataFrame con los datos
            season (str): Temporada
            season_type (str): Tipo de temporada
            url (str): URL de origen

        Returns:
            list: Lista de objetos BoxScore
        """
        boxscore_objects = []

        try:
            for row in df.iter_rows(named=True):
                try:
                    # Mapear campos del DataFrame al modelo
                    # Extraer datos básicos
                    team = row.get("Team") or row.get("TEAM", "")
                    match_up = row.get("Match Up") or row.get("MATCH UP", "")
                    game_date_str = row.get("Game Date") or row.get("GDATE", "")
                    win_lose = row.get("W/L") or row.get("W-L", "")

                    # Extraer game_id si existe
                    game_id_from_row = row.get("game_id") or row.get("GAME_ID") or None

                    # Parsear fecha
                    game_date = self._parse_game_date(game_date_str)

                    if not game_date:
                        logger.warning(f"No se pudo parsear fecha para fila: {row}")
                        continue

                    # Usar game_id si está disponible, sino crear uno basado en fecha, equipo, etc.
                    if game_id_from_row and str(game_id_from_row).strip():
                        match_id = str(game_id_from_row).strip()
                    else:
                        # Fallback: crear match_id único
                        match_id = f"{season}_{season_type}_{game_date}_{team}"

                    # Convertir valores numéricos
                    def safe_int(value):
                        try:
                            if value is None or value == "":
                                return 0
                            return int(
                                float(str(value).replace("%", "").replace(",", ""))
                            )
                        except (ValueError, TypeError):
                            return 0

                    def safe_float(value):
                        try:
                            if value is None or value == "":
                                return 0.0
                            return float(str(value).replace("%", "").replace(",", ""))
                        except (ValueError, TypeError):
                            return 0.0

                    # Crear objeto BoxScore
                    boxscore = BoxScore(
                        season=season,
                        season_type=season_type,
                        match_id=match_id,
                        team=str(team)[:10],  # Limitar a max_length
                        match_up=str(match_up)[:50],
                        game_date=game_date,
                        win_lose=str(win_lose)[:1] if win_lose else "",
                        min=safe_int(row.get("MIN")),
                        pts=safe_int(row.get("PTS")),
                        fgm=safe_int(row.get("FGM")),
                        fga=safe_int(row.get("FGA")),
                        fg_percent=safe_float(row.get("FG%")),
                        threepm=safe_int(row.get("3PM")),
                        threepa=safe_int(row.get("3PA")),
                        threep_percent=safe_float(row.get("3P%")),
                        ftm=safe_int(row.get("FTM")),
                        fta=safe_int(row.get("FTA")),
                        ft_percent=safe_float(row.get("FT%")),
                        oreb=safe_int(row.get("OREB")),
                        dreb=safe_int(row.get("DREB")),
                        reb=safe_int(row.get("REB")),
                        ast=safe_int(row.get("AST")),
                        stl=safe_int(row.get("STL")),
                        blk=safe_int(row.get("BLK")),
                        tov=safe_int(row.get("TOV")),
                        pf=safe_int(row.get("PF")),
                        plus_minus=safe_int(row.get("PLUS_MINUS")),
                    )

                    boxscore_objects.append(boxscore)

                except Exception as e:
                    logger.error(f"Error mapeando fila a BoxScore: {e} - Fila: {row}")
                    continue

        except Exception as e:
            logger.error(f"Error mapeando DataFrame a BoxScore: {e}")
            return []

        return boxscore_objects

    def save_to_database(self, data, url, season=None, season_type=None):
        """
        Guarda los datos extraídos en la base de datos Django

        Args:
            data (pl.DataFrame): DataFrame con los datos extraídos
            url (str): URL de origen
            season (str, optional): Temporada. Si es None, se extrae de la URL
            season_type (str, optional): Tipo de temporada. Si es None, se extrae de la URL

        Returns:
            tuple: (success (bool), count (int)) - True si se guardó exitosamente y cantidad guardada
        """
        try:
            if data.empty:
                logger.warning("No hay datos para guardar en la base de datos")
                return False, 0

            # Extraer season y season_type de la URL si no se proporcionaron
            if not season or not season_type:
                url_season, url_season_type = self._extract_url_params(url)
                season = season or url_season
                season_type = season_type or url_season_type

            if not season or not season_type:
                logger.error(
                    f"No se pudo determinar season y season_type para URL: {url}"
                )
                return False, 0

            # Mapear DataFrame a objetos BoxScore
            boxscore_objects = self._map_dataframe_to_model(
                data, season, season_type, url
            )

            if not boxscore_objects:
                logger.warning("No se pudieron mapear datos a objetos BoxScore")
                return False, 0

            # Guardar en la base de datos usando bulk_create con ignore_conflicts
            # para evitar duplicados basados en match_id (unique)
            saved_count = 0
            with transaction.atomic():
                # Dividir en lotes para evitar problemas de memoria
                batch_size = 100
                for i in range(0, len(boxscore_objects), batch_size):
                    batch = boxscore_objects[i : i + batch_size]
                    # Usar update_or_create para manejar duplicados
                    for obj in batch:
                        _, created = BoxScore.objects.update_or_create(
                            match_id=obj.match_id,
                            defaults={
                                "season": obj.season,
                                "season_type": obj.season_type,
                                "team": obj.team,
                                "match_up": obj.match_up,
                                "game_date": obj.game_date,
                                "win_lose": obj.win_lose,
                                "min": obj.min,
                                "pts": obj.pts,
                                "fgm": obj.fgm,
                                "fga": obj.fga,
                                "fg_percent": obj.fg_percent,
                                "threepm": obj.threepm,
                                "threepa": obj.threepa,
                                "threep_percent": obj.threep_percent,
                                "ftm": obj.ftm,
                                "fta": obj.fta,
                                "ft_percent": obj.ft_percent,
                                "oreb": obj.oreb,
                                "dreb": obj.dreb,
                                "reb": obj.reb,
                                "ast": obj.ast,
                                "stl": obj.stl,
                                "blk": obj.blk,
                                "tov": obj.tov,
                                "pf": obj.pf,
                                "plus_minus": obj.plus_minus,
                            },
                        )
                        if created:
                            saved_count += 1

            logger.info(
                f"Guardados {saved_count} registros de BoxScore en la base de datos (de {len(boxscore_objects)} totales)"
            )
            return True, saved_count

        except Exception as e:
            logger.error(f"Error guardando datos en la base de datos: {e}")
            return False, 0

    def process_links(self, urls):
        """
        Procesa una lista de URLs, scrapea los datos y los guarda en la base de datos

        Args:
            urls: Lista de URLs (strings)

        Returns:
            dict: Estadísticas del procesamiento
        """
        stats = {
            "total": 0,
            "processed": 0,
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "total_records_saved": 0,
        }

        try:
            # Convertir a lista si no lo es
            if not isinstance(urls, list):
                urls = list(urls)

            stats["total"] = len(urls)

            logger.info(f"Iniciando procesamiento de {stats['total']} links")

            # Conectar el driver
            if not self.connect():
                logger.error("No se pudo conectar el driver")
                return stats

            for i, url in enumerate(urls, 1):
                stats["processed"] += 1

                try:
                    # Extraer información de la URL
                    season, season_type = self._extract_url_params(url)
                    parsed = urlparse(url)
                    category = parsed.path.split("/")[-1]

                    logger.info(
                        f"Procesando link {i}/{stats['total']}: {category} - {season} - {season_type}"
                    )

                    # Buscar el objeto Links para verificar si ya fue scrapeado
                    try:
                        link_obj = Links.objects.get(url=url)
                        if link_obj.scraped:
                            logger.info(f"Link ya scrapeado, saltando: {url}")
                            stats["skipped"] += 1
                            continue
                    except Links.DoesNotExist:
                        # Si no existe el objeto, continuar de todas formas
                        logger.warning(f"Link no encontrado en BD: {url}")

                    # Registrar inicio del scraping
                    log_entry = ScrapperLogs.objects.create(
                        url=url,
                        category=category,
                        season=season or "",
                        season_type=season_type or "",
                        status="processing",
                    )

                    # Extraer datos de la URL
                    data = self.extract_table_data(url)

                    if data.empty:
                        logger.warning(f"No se extrajeron datos de: {url}")
                        log_entry.status = "failed"
                        log_entry.error = "No se extrajeron datos"
                        log_entry.save()
                        stats["failed"] += 1
                        continue

                    # Guardar en la base de datos
                    success, count = self.save_to_database(
                        data, url, season, season_type
                    )

                    if success:
                        # Marcar link como scrapeado si existe
                        try:
                            link_obj = Links.objects.get(url=url)
                            link_obj.scraped = True
                            link_obj.save()
                        except Links.DoesNotExist:
                            pass

                        # Actualizar log
                        log_entry.status = "success"
                        log_entry.save()

                        stats["success"] += 1
                        stats["total_records_saved"] += count

                        logger.info(
                            f"✅ Link procesado exitosamente: {count} registros guardados"
                        )
                    else:
                        log_entry.status = "failed"
                        log_entry.error = "Error guardando en base de datos"
                        log_entry.save()
                        stats["failed"] += 1
                        logger.error(f"❌ Error guardando datos de: {url}")

                    # Pausa entre requests
                    time.sleep(2)

                except Exception as e:
                    logger.error(f"Error procesando link {url}: {e}")
                    stats["failed"] += 1

                    # Registrar error en log
                    try:
                        parsed = urlparse(url)
                        category = parsed.path.split("/")[-1]
                        season, season_type = self._extract_url_params(url)
                        log_entry = ScrapperLogs.objects.create(
                            url=url,
                            category=category,
                            season=season or "",
                            season_type=season_type or "",
                            status="failed",
                            error=str(e),
                        )
                    except Exception:
                        pass

            # Desconectar el driver
            self.disconnect()

            logger.info(
                f"Procesamiento completado: {stats['success']} exitosos, {stats['failed']} fallidos, {stats['skipped']} omitidos"
            )

        except Exception as e:
            logger.error(f"Error en process_links: {e}")
            self.disconnect()

        return stats
