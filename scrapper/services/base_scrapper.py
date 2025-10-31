#!/usr/bin/env python3
"""
Clase base para todos los scrapers de NBA Stats
Contiene la funcionalidad común a todas las categorías

OPTIMIZADO PARA DOCKER CON PYTHON 3.15:
- Configuraciones específicas para contenedores
- Manejo robusto de timeouts y reintentos
- Optimizaciones de memoria para entornos containerizados
- User agent actualizado para evitar detección
- Configuraciones de Chrome optimizadas para Docker
"""

import logging
import os
import time
from abc import ABC, abstractmethod

import polars as pl
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """
    Clase base abstracta para todos los scrapers de NBA Stats
    """

    def __init__(self, headless=True, wait_timeout=15):
        """
        Inicializa el scraper base para Docker con Python 3.15

        Args:
            headless (bool): Si ejecutar el navegador en modo headless (siempre True en Docker)
            wait_timeout (int): Tiempo de espera para elementos (aumentado para Docker)
        """
        # En Docker, siempre headless
        self.headless = True if headless else True
        self.wait_timeout = wait_timeout
        self.driver = None
        self.base_url = "https://www.nba.com/stats/teams/"
        self.wait = None

        # Configuraciones específicas para Docker
        self.docker_mode = True
        self.max_retries = 3
        self.retry_delay = 2

    def _setup_driver(self):
        """
        Configura el driver de Selenium para Docker con Python 3.15
        """
        try:
            chrome_options = Options()

            # Configuraciones obligatorias para Docker
            chrome_options.add_argument("--headless")  # Siempre headless en Docker
            chrome_options.add_argument("--no-sandbox")  # Requerido para Docker
            chrome_options.add_argument(
                "--disable-dev-shm-usage"
            )  # Evita problemas de memoria
            chrome_options.add_argument("--disable-gpu")  # Sin GPU en contenedores
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-features=TranslateUI")
            chrome_options.add_argument("--disable-ipc-flooding-protection")

            # Configuraciones de ventana para Docker
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--start-maximized")

            # User agent para evitar detección
            chrome_options.add_argument(
                "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )

            # Configuraciones adicionales para estabilidad en Docker
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument(
                "--disable-images"
            )  # Opcional: acelera la carga
            chrome_options.add_argument(
                "--disable-javascript"
            )  # Opcional: si no necesitas JS

            # Configuraciones de red para Docker
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")

            # Configurar timeouts para entornos Docker
            chrome_options.add_argument("--timeout=30000")
            chrome_options.add_argument("--page-load-strategy=normal")

            self.driver = webdriver.Chrome(options=chrome_options)

            # Configurar timeouts específicos para Docker
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)

            self.wait = WebDriverWait(self.driver, self.wait_timeout)

            logger.info("Driver configurado exitosamente para Docker")
            return True

        except Exception as e:
            logger.error(f"Error configurando el driver para Docker: {e}")
            return False

    def connect(self):
        """
        Establece la conexión con el navegador
        """
        if not self.driver:
            return self._setup_driver()
        return True

    def disconnect(self):
        """
        Cierra la conexión con el navegador
        """
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("Conexión cerrada")

    def read_links_file(self, file_path):
        """
        Lee un archivo de enlaces y retorna la lista de URLs

        Args:
            file_path (str): Ruta al archivo de enlaces

        Returns:
            list: Lista de URLs
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"Archivo no encontrado: {file_path}")
                return []

            with open(file_path, "r", encoding="utf-8") as f:
                urls = [line.strip() for line in f if line.strip()]

            logger.info(f"Leídos {len(urls)} enlaces de {file_path}")
            return urls

        except Exception as e:
            logger.error(f"Error leyendo archivo {file_path}: {e}")
            return []

    def navigate_to_url(self, url):
        """
        Navega a una URL específica con reintentos para Docker

        Args:
            url (str): URL a navegar

        Returns:
            bool: True si la navegación fue exitosa
        """
        for attempt in range(self.max_retries):
            try:
                if not self.driver:
                    if not self.connect():
                        return False

                logger.info(
                    f"Intentando navegar a: {url} (intento {attempt + 1}/{self.max_retries})"
                )

                self.driver.get(url)

                # Espera más larga para Docker
                time.sleep(3)

                # Verificar que la página cargó correctamente
                if "nba.com" not in self.driver.current_url:
                    raise Exception("No se pudo cargar la página NBA")

                # Esperar a que la tabla esté presente
                table_selector = self.get_table_selector()
                if table_selector:
                    self.wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, table_selector)
                        )
                    )

                logger.info(f"Navegación exitosa a: {url}")
                return True

            except TimeoutException:
                logger.warning(f"Timeout en intento {attempt + 1} para: {url}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    logger.error(f"Timeout final esperando elementos en: {url}")
                    return False
            except Exception as e:
                logger.warning(f"Error en intento {attempt + 1} para {url}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    logger.error(f"Error final navegando a {url}: {e}")
                    return False

        return False

    def extract_table_data(self, url):
        """
        Extrae datos de la tabla en la URL actual

        Args:
            url (str): URL actual

        Returns:
            pl.DataFrame: Datos extraídos
        """
        try:
            if not self.navigate_to_url(url):
                return pl.DataFrame()

            # Verificar si la página muestra "No data available"
            if self._has_no_data():
                logger.warning(f"No hay datos disponibles en: {url}")
                return pl.DataFrame()

            # Obtener el selector específico de la categoría
            table_selector = self.get_table_selector()
            if not table_selector:
                logger.error("Selector de tabla no definido")
                return pl.DataFrame()

            # Esperar a que la tabla esté presente
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, table_selector))
            )

            # Extraer datos usando el método específico de la categoría
            data = self.extract_data(url)

            if not data.empty:
                logger.info(f"Extraídos {len(data)} registros de {url}")
            else:
                logger.warning(f"No se extrajeron datos de {url}")

            return data

        except TimeoutException:
            logger.error(f"Timeout extrayendo datos de: {url}")
            return pl.DataFrame()
        except Exception as e:
            logger.error(f"Error extrayendo datos de {url}: {e}")
            return pl.DataFrame()

    def scrape_links_file(self, file_path):
        """
        Scrapea todos los enlaces de un archivo

        Args:
            file_path (str): Ruta al archivo de enlaces

        Returns:
            pl.DataFrame: Datos combinados de todos los enlaces
        """
        try:
            urls = self.read_links_file(file_path)
            if not urls:
                return pl.DataFrame()

            all_data = []

            for i, url in enumerate(urls, 1):
                logger.info(f"Procesando enlace {i}/{len(urls)}: {url}")

                data = self.extract_table_data(url)
                if not data.empty:
                    all_data.append(data)
                    logger.info(f"✅ Datos extraídos exitosamente de {url}")
                else:
                    logger.warning(f"⚠️ No se extrajeron datos de {url}")

                # Pausa más larga entre requests para Docker
                time.sleep(2)

                # Limpiar memoria periódicamente en Docker
                if i % 10 == 0:
                    logger.info("🧹 Limpiando memoria...")
                    if self.driver:
                        self.driver.execute_script("window.gc && window.gc();")

            if all_data:
                combined_data = pl.concat(all_data)
                logger.info(f"Total de registros extraídos: {len(combined_data)}")
                return combined_data
            else:
                logger.warning("No se extrajeron datos de ningún enlace")
                return pl.DataFrame()

        except Exception as e:
            logger.error(f"Error en scrape_links_file: {e}")
            return pl.DataFrame()

    def save_data(self, data, output_path):
        """
        Guarda los datos en un archivo CSV

        Args:
            data (pl.DataFrame): Datos a guardar
            output_path (str): Ruta de salida

        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            if data.empty:
                logger.warning("No hay datos para guardar")
                return False

            # Crear directorio si no existe
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            data.write_csv(output_path)
            logger.info(f"Datos guardados en: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error guardando datos: {e}")
            return False

    def _has_no_data(self):
        """
        Verifica si la página muestra el mensaje "No data available"

        Returns:
            bool: True si no hay datos disponibles
        """
        try:
            no_data_element = self.driver.find_element(
                By.CSS_SELECTOR, ".NoDataMessage_base__xUA61"
            )
            return no_data_element.is_displayed()
        except NoSuchElementException:
            return False
        except Exception as e:
            logger.warning(f"Error verificando si hay datos: {e}")
            return False

    @abstractmethod
    def get_table_selector(self):
        """
        Retorna el selector CSS para la tabla específica de esta categoría

        Returns:
            str: Selector CSS de la tabla
        """

    @abstractmethod
    def extract_data(self, url):
        """
        Extrae datos específicos de la tabla

        Args:
            url (str): URL actual

        Returns:
            pl.DataFrame: Datos extraídos
        """

    def get_category_name(self):
        """
        Retorna el nombre de la categoría

        Returns:
            str: Nombre de la categoría
        """
        return self.__class__.__name__.replace("Scraper", "").lower()

    def check_docker_compatibility(self):
        """
        Verifica la compatibilidad con Docker y Python 3.15

        Returns:
            dict: Información de compatibilidad
        """
        import platform
        import sys

        compatibility_info = {
            "python_version": sys.version,
            "platform": platform.platform(),
            "docker_mode": self.docker_mode,
            "headless": self.headless,
            "wait_timeout": self.wait_timeout,
            "max_retries": self.max_retries,
        }

        logger.info(f"🐳 Modo Docker activado: {self.docker_mode}")
        logger.info(f"🐍 Python version: {sys.version}")
        logger.info(f"🖥️ Platform: {platform.platform()}")

        return compatibility_info

    def __enter__(self):
        """
        Context manager entry
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit
        """
        self.disconnect()
