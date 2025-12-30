from .base import BaseModel
from sklearn.ensemble import VotingClassifier as SklearnVotingClassifier
from sklearn.ensemble import StackingClassifier as SklearnStackingClassifier
from sklearn.ensemble import BaggingClassifier as SklearnBaggingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report


class VotingClassifier(BaseModel):
    def __init__(self, X, y, estimators=None, **kwargs):
        super().__init__(X, y, **kwargs)
        self.estimators = estimators or [
            ("lr", LogisticRegression(random_state=self.random_state)),
            ("dt", DecisionTreeClassifier(random_state=self.random_state)),
        ]
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        self.model = SklearnVotingClassifier(estimators=self.estimators, voting="hard")

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
        return {"accuracy": accuracy, "classification_report": report}


class StackingClassifier(BaseModel):
    def __init__(self, X, y, estimators=None, final_estimator=None, **kwargs):
        super().__init__(X, y, **kwargs)
        self.estimators = estimators or [
            ("lr", LogisticRegression(random_state=self.random_state)),
            ("dt", DecisionTreeClassifier(random_state=self.random_state)),
        ]
        self.final_estimator = final_estimator or LogisticRegression(
            random_state=self.random_state
        )
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        self.model = SklearnStackingClassifier(
            estimators=self.estimators, final_estimator=self.final_estimator
        )

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
        return {"accuracy": accuracy, "classification_report": report}


class BaggingClassifier(BaseModel):
    def __init__(self, X, y, base_estimator=None, **kwargs):
        super().__init__(X, y, **kwargs)
        self.base_estimator = base_estimator or DecisionTreeClassifier(
            random_state=self.random_state
        )
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        self.model = SklearnBaggingClassifier(
            base_estimator=self.base_estimator, random_state=self.random_state
        )

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
        return {"accuracy": accuracy, "classification_report": report}


class AdaBoost(BaseModel):
    def __init__(self, X, y, base_estimator=None, **kwargs):
        super().__init__(X, y, **kwargs)
        self.base_estimator = base_estimator or DecisionTreeClassifier(
            random_state=self.random_state
        )
        self.prepare_data()
        self._build_model()

    def _build_model(self):
        from sklearn.ensemble import AdaBoostClassifier as SklearnAdaBoostClassifier

        self.model = SklearnAdaBoostClassifier(
            base_estimator=self.base_estimator, random_state=self.random_state
        )

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
        return {"accuracy": accuracy, "classification_report": report}
