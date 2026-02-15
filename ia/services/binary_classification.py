from .base import BaseModel
from sklearn.linear_model import LogisticRegression as SklearnLogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score


class LogisticRegression(BaseModel):
    def __init__(self, X, y, **kwargs):
        super().__init__(X, y, **kwargs)
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        self.model = SklearnLogisticRegression(random_state=self.random_state)

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


class SVM(BaseModel):
    def __init__(self, X, y, **kwargs):
        super().__init__(X, y, **kwargs)
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        self.model = SVC(random_state=self.random_state, probability=True)

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


class NaiveBayes(BaseModel):
    def __init__(self, X, y, **kwargs):
        super().__init__(X, y, **kwargs)
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        self.model = GaussianNB()

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


class GradientBoosting(BaseModel):
    def __init__(self, X, y, **kwargs):
        super().__init__(X, y, **kwargs)
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        self.model = GradientBoostingClassifier(random_state=self.random_state)

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
        accuracy = accuracy_score(self.y_test, y_pred)
        report = classification_report(self.y_test, y_pred, output_dict=True)
        try:
            y_proba = self.model.predict_proba(self.X_test)[:, 1]
            roc_auc = roc_auc_score(self.y_test, y_proba)
            return {"accuracy": accuracy, "roc_auc": roc_auc, "classification_report": report}
        except:
            return {"accuracy": accuracy, "classification_report": report}
