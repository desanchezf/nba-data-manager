from .base import BaseModel
from sklearn.linear_model import LinearRegression as SklearnLinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor as SklearnRandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


class LinearRegression(BaseModel):
    def __init__(self, X, y, **kwargs):
        super().__init__(X, y, **kwargs)
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        self.model = SklearnLinearRegression()

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


class RidgeRegression(BaseModel):
    def __init__(self, X, y, **kwargs):
        super().__init__(X, y, **kwargs)
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        self.model = Ridge(random_state=self.random_state)

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


class LassoRegression(BaseModel):
    def __init__(self, X, y, **kwargs):
        super().__init__(X, y, **kwargs)
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        self.model = Lasso(random_state=self.random_state)

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


class RandomForestRegressor(BaseModel):
    def __init__(self, X, y, **kwargs):
        super().__init__(X, y, **kwargs)
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        self.model = SklearnRandomForestRegressor(random_state=self.random_state)

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
        mse = mean_squared_error(self.y_test, y_pred)
        mae = mean_absolute_error(self.y_test, y_pred)
        r2 = r2_score(self.y_test, y_pred)
        return {"mse": mse, "mae": mae, "r2": r2, "rmse": mse ** 0.5}


class XGBoostRegressor(BaseModel):
    def __init__(self, X, y, **kwargs):
        super().__init__(X, y, **kwargs)
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        self.model = XGBRegressor(random_state=self.random_state)

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
        mse = mean_squared_error(self.y_test, y_pred)
        mae = mean_absolute_error(self.y_test, y_pred)
        r2 = r2_score(self.y_test, y_pred)
        return {"mse": mse, "mae": mae, "r2": r2, "rmse": mse ** 0.5}


class LightGBMRegressor(BaseModel):
    def __init__(self, X, y, **kwargs):
        super().__init__(X, y, **kwargs)
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        self.model = LGBMRegressor(random_state=self.random_state)

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
        mse = mean_squared_error(self.y_test, y_pred)
        mae = mean_absolute_error(self.y_test, y_pred)
        r2 = r2_score(self.y_test, y_pred)
        return {"mse": mse, "mae": mae, "r2": r2, "rmse": mse ** 0.5}
