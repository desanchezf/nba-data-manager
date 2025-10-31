#!/usr/bin/env python3
"""
Scraper especializado para datos de Boxscore de NBA
"""

import logging
import time

import polars as pl
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
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
                tbody = table.find_element(By.TAG_NAME, "tbody")
                data_rows = tbody.find_elements(By.TAG_NAME, "tr")

                for row in data_rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    row_data = []

                    for cell in cells:
                        # Manejar celdas que pueden contener enlaces
                        # Extraer el texto del enlace si existe, sino el texto de la celda
                        try:
                            link = cell.find_element(By.TAG_NAME, "a")
                            cell_text = link.text.strip()
                        except NoSuchElementException:
                            cell_text = cell.text.strip()
                        
                        row_data.append(cell_text)

                    if row_data:  # Solo agregar filas con datos
                        rows.append(row_data)

                # Crear DataFrame para esta página
                if rows and headers:
                    df = pl.DataFrame(rows, columns=headers)

                    # Agregar metadatos
                    df = df.with_columns(pl.lit(url).alias("source_url"))
                    df = df.with_columns(pl.lit("boxscore").alias("category"))
                    df = df.with_columns(pl.lit(page_number).alias("page_number"))

                    # Limpiar datos
                    df = self._clean_data(df)

                    all_dataframes.append(df)
                    logger.info(f"Extraídos {len(df)} registros de la página {page_number}")

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
                logger.info(f"Total de registros extraídos: {len(combined_df)} de {page_number} página(s)")
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
                "+/-",
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
                    df = df.with_columns(
                        pl.col(col).str.strip_chars().alias(col)
                    )

            # Limpiar fechas (puede ser "Game Date" o similar)
            date_cols = ["Game Date", "GDATE"]
            for col in date_cols:
                if col in df.columns:
                    df = df.with_columns(
                        pl.col(col).str.strip_chars().alias(col)
                    )

            # Agregar timestamp
            df = df.with_columns(
                pl.lit(pl.datetime.now()).alias("scraped_at")
            )

            return df

        except Exception as e:
            logger.error(f"Error limpiando datos: {e}")
            return df



