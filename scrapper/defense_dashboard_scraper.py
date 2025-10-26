#!/usr/bin/env python3
"""
Scraper especializado para datos de Defense Dashboard de NBA
"""

import polars as pl
from selenium.webdriver.common.by import By

from .base_scraper import BaseNBAScraper


class DefenseDashboardScraper(BaseNBAScraper):
    """
    Scraper especializado para datos de Defense Dashboard
    """

    def get_table_selector(self):
        """
        Selector específico para la tabla de Defense Dashboard
        """
        return "table[data-module='DefenseDashboard']"

    def extract_data(self, url):
        """
        Extrae datos específicos de Defense Dashboard

        Args:
            url (str): URL actual

        Returns:
            pl.DataFrame: Datos extraídos
        """
        try:
            # Buscar la tabla de datos
            table = self.driver.find_element(By.CSS_SELECTOR, self.get_table_selector())

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
                    row_data.append(cell.text.strip())

                if row_data:  # Solo agregar filas con datos
                    rows.append(row_data)

            # Crear DataFrame
            if rows and headers:
                df = pl.DataFrame(rows, columns=headers)

                # Agregar metadatos
                df = df.with_columns(pl.lit(url).alias("source_url"))
                df = df.with_columns(pl.lit("defense_dashboard").alias("category"))

                # Limpiar datos
                df = self._clean_data(df)

                return df
            else:
                return pl.DataFrame()

        except Exception as e:
            self.logger.error(f"Error extrayendo datos de Defense Dashboard: {e}")
            return pl.DataFrame()

    def _clean_data(self, df):
        """
        Limpia y procesa los datos específicos de Defense Dashboard

        Args:
            df (pl.DataFrame): DataFrame a limpiar

        Returns:
            pl.DataFrame: DataFrame limpio
        """
        try:
            # Convertir columnas numéricas específicas de Defense Dashboard
            numeric_columns = [
                "OPP_FGM",
                "OPP_FGA",
                "OPP_FG%",
                "OPP_3PM",
                "OPP_3PA",
                "OPP_3P%",
                "OPP_PTS",
                "OPP_PTS%",
                "OPP_EFG%",
                "OPP_TS%",
                "OPP_PACE",
                "DEF_RATING",
                "DEF_RANK",
                "OPP_TOV%",
                "OPP_STL%",
                "OPP_BLK%",
            ]

            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pl.col().cast(pl.Float64, strict=False)(df[col], errors="coerce")

            # Limpiar nombres de equipos
            if "TEAM" in df.columns:
                df = df.with_columns(pl.lit(pl.col("TEAM").str.strip_chars()).alias("TEAM"))

            # Agregar timestamp
            df = df.with_columns(pl.lit(pl.datetime.now()).alias("scraped_at"))

            return df

        except Exception as e:
            self.logger.error(f"Error limpiando datos: {e}")
            return df
