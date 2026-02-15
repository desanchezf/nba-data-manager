from .base import BaseModel
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score


class MLP(BaseModel):
    def __init__(self, X, y, problem_type="classification", **kwargs):
        super().__init__(X, y, **kwargs)
        self.problem_type = problem_type
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        if self.problem_type == "classification":
            self.model = MLPClassifier(random_state=self.random_state, max_iter=1000)
        else:
            self.model = MLPRegressor(random_state=self.random_state, max_iter=1000)

    def fit(self):
        self.model.fit(self.X_train, self.y_train)
        self.is_trained = True

    def predict(self, X=None):
        if not self.is_trained:
            raise ValueError("El modelo debe estar entrenado antes de predecir")
        X = X if X is not None else self.X_test
        if self.scaler and X is not self.X_test:
            X = self.scaler.transform(X)
        return self.model.predict(X)

    def evaluate(self, metrics=None):
        if not self.is_trained:
            raise ValueError("El modelo debe estar entrenado antes de evaluarlo")
        y_pred = self.predict()
        if self.problem_type == "classification":
            accuracy = accuracy_score(self.y_test, y_pred)
            report = classification_report(self.y_test, y_pred, output_dict=True)
            return {"accuracy": accuracy, "classification_report": report}
        else:
            mse = mean_squared_error(self.y_test, y_pred)
            r2 = r2_score(self.y_test, y_pred)
            return {"mse": mse, "r2": r2, "rmse": mse ** 0.5}


class CNN(BaseModel):
    def __init__(self, X, y, **kwargs):
        super().__init__(X, y, **kwargs)
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        # Placeholder para CNN - requiere TensorFlow/Keras
        self.model = None

    def fit(self):
        # Implementación pendiente - requiere TensorFlow/Keras
        raise NotImplementedError("CNN requiere implementación con TensorFlow/Keras")

    def predict(self, X=None):
        if not self.is_trained:
            raise ValueError("El modelo debe estar entrenado antes de predecir")
        raise NotImplementedError("CNN requiere implementación con TensorFlow/Keras")

    def evaluate(self, metrics=None):
        if not self.is_trained:
            raise ValueError("El modelo debe estar entrenado antes de evaluarlo")
        raise NotImplementedError("CNN requiere implementación con TensorFlow/Keras")


class RNN(BaseModel):
    def __init__(self, X, y, **kwargs):
        super().__init__(X, y, **kwargs)
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        # Placeholder para RNN - requiere TensorFlow/Keras
        self.model = None

    def fit(self):
        # Implementación pendiente - requiere TensorFlow/Keras
        raise NotImplementedError("RNN requiere implementación con TensorFlow/Keras")

    def predict(self, X=None):
        if not self.is_trained:
            raise ValueError("El modelo debe estar entrenado antes de predecir")
        raise NotImplementedError("RNN requiere implementación con TensorFlow/Keras")

    def evaluate(self, metrics=None):
        if not self.is_trained:
            raise ValueError("El modelo debe estar entrenado antes de evaluarlo")
        raise NotImplementedError("RNN requiere implementación con TensorFlow/Keras")


class LSTM(BaseModel):
    def __init__(self, X, y, **kwargs):
        super().__init__(X, y, **kwargs)
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        # Placeholder para LSTM - requiere TensorFlow/Keras
        self.model = None

    def fit(self):
        # Implementación pendiente - requiere TensorFlow/Keras
        raise NotImplementedError("LSTM requiere implementación con TensorFlow/Keras")

    def predict(self, X=None):
        if not self.is_trained:
            raise ValueError("El modelo debe estar entrenado antes de predecir")
        raise NotImplementedError("LSTM requiere implementación con TensorFlow/Keras")

    def evaluate(self, metrics=None):
        if not self.is_trained:
            raise ValueError("El modelo debe estar entrenado antes de evaluarlo")
        raise NotImplementedError("LSTM requiere implementación con TensorFlow/Keras")


class GRU(BaseModel):
    def __init__(self, X, y, **kwargs):
        super().__init__(X, y, **kwargs)
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        # Placeholder para GRU - requiere TensorFlow/Keras
        self.model = None

    def fit(self):
        # Implementación pendiente - requiere TensorFlow/Keras
        raise NotImplementedError("GRU requiere implementación con TensorFlow/Keras")

    def predict(self, X=None):
        if not self.is_trained:
            raise ValueError("El modelo debe estar entrenado antes de predecir")
        raise NotImplementedError("GRU requiere implementación con TensorFlow/Keras")

    def evaluate(self, metrics=None):
        if not self.is_trained:
            raise ValueError("El modelo debe estar entrenado antes de evaluarlo")
        raise NotImplementedError("GRU requiere implementación con TensorFlow/Keras")
