from abc import ABC, abstractmethod
import pickle
import os
from typing import Optional, Tuple
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger(__name__)


class BaseModel(ABC):
    """
    Clase base abstracta para todos los modelos de Machine Learning.
    Proporciona funcionalidad común: carga de datos, preprocesamiento,
    división train/test, guardado/carga de modelos, evaluación básica.
    """

    def __init__(self, X, y, test_size: float = 0.2, random_state: int = 42,
                 normalize: bool = True, model_name: Optional[str] = None):
        """
        Inicializa el modelo base.

        Args:
            X: Features (datos de entrada)
            y: Target (variable objetivo)
            test_size: Proporción del dataset para test (default: 0.2)
            random_state: Semilla para reproducibilidad (default: 42)
            normalize: Si True, normaliza los datos (default: True)
            model_name: Nombre del modelo para guardado/carga (default: None)
        """
        self.X = X
        self.y = y
        self.test_size = test_size
        self.random_state = random_state
        self.normalize = normalize
        self.model_name = model_name or self.__class__.__name__

        # Atributos que se inicializan en prepare_data
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = None
        self.model = None
        self.is_trained = False

    def prepare_data(self):
        """
        Prepara los datos: división train/test y normalización si es necesario.
        """
        logger.info(f"Preparando datos para {self.model_name}")

        # Validación básica
        if self.X is None or self.y is None:
            raise ValueError("X e y no pueden ser None")

        if len(self.X) != len(self.y):
            raise ValueError("X e y deben tener la misma longitud")

        # División train/test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=self.test_size, random_state=self.random_state
        )

        logger.info(f"Datos divididos: Train={len(self.X_train)}, Test={len(self.X_test)}")

        # Normalización
        if self.normalize:
            self.scaler = StandardScaler()
            self.X_train = self.scaler.fit_transform(self.X_train)
            self.X_test = self.scaler.transform(self.X_test)
            logger.info("Datos normalizados")

    @abstractmethod
    def _build_model(self):
        """
        Construye el modelo específico. Debe ser implementado por cada subclase.
        """
        pass

    @abstractmethod
    def fit(self):
        """
        Entrena el modelo. Debe ser implementado por cada subclase.
        """
        pass

    @abstractmethod
    def predict(self, X=None):
        """
        Realiza predicciones. Debe ser implementado por cada subclase.

        Args:
            X: Datos para predecir. Si None, usa X_test.

        Returns:
            Predicciones
        """
        pass

    def save_model(self, filepath: str):
        """
        Guarda el modelo entrenado y el scaler si existe.

        Args:
            filepath: Ruta donde guardar el modelo
        """
        if not self.is_trained:
            raise ValueError("El modelo debe estar entrenado antes de guardarlo")

        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'model_name': self.model_name,
            'is_trained': self.is_trained
        }

        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

        logger.info(f"Modelo guardado en {filepath}")

    def load_model(self, filepath: str):
        """
        Carga un modelo previamente guardado.

        Args:
            filepath: Ruta del modelo guardado
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Modelo no encontrado en {filepath}")

        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)

        self.model = model_data['model']
        self.scaler = model_data.get('scaler')
        self.model_name = model_data.get('model_name', self.model_name)
        self.is_trained = model_data.get('is_trained', False)

        logger.info(f"Modelo cargado desde {filepath}")

    def evaluate(self, metrics: Optional[list] = None):
        """
        Evalúa el modelo. Debe ser implementado por subclases específicas
        según el tipo de problema (clasificación, regresión, etc.).

        Args:
            metrics: Lista de métricas a calcular. Si None, usa métricas por defecto.

        Returns:
            Diccionario con las métricas calculadas
        """
        if not self.is_trained:
            raise ValueError("El modelo debe estar entrenado antes de evaluarlo")

        logger.warning("evaluate() debe ser implementado por la subclase específica")
        return {}

    def get_model_info(self) -> dict:
        """
        Retorna información sobre el modelo.

        Returns:
            Diccionario con información del modelo
        """
        return {
            'model_name': self.model_name,
            'is_trained': self.is_trained,
            'normalize': self.normalize,
            'test_size': self.test_size,
            'random_state': self.random_state,
            'train_size': len(self.X_train) if self.X_train is not None else None,
            'test_size': len(self.X_test) if self.X_test is not None else None
        }
