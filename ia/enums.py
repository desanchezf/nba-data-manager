from django.utils.translation import gettext_lazy as _


class AlgorithmChoices:
    """Tipos de algoritmos de Machine Learning"""

    LOGISTIC_REGRESSION = "logistic_regression"
    RANDOM_FOREST = "random_forest"
    XGBOOST = "xgboost"
    LIGHTGBM = "lightgbm"
    SVM = "svm"
    NAIVE_BAYES = "naive_bayes"
    GRADIENT_BOOSTING = "gradient_boosting"
    LINEAR_REGRESSION = "linear_regression"
    RIDGE_REGRESSION = "ridge_regression"
    LASSO_REGRESSION = "lasso_regression"
    MLP = "mlp"
    CNN = "cnn"
    RNN = "rnn"
    LSTM = "lstm"
    GRU = "gru"
    VOTING_CLASSIFIER = "voting_classifier"
    STACKING_CLASSIFIER = "stacking_classifier"
    BAGGING_CLASSIFIER = "bagging_classifier"
    ADABOOST = "adaboost"
    ELO = "elo"
    GLICKO = "glicko"
    TRUESKILL = "trueskill"

    CHOICES = (
        (LOGISTIC_REGRESSION, _("Logistic Regression")),
        (RANDOM_FOREST, _("Random Forest")),
        (XGBOOST, _("XGBoost")),
        (LIGHTGBM, _("LightGBM")),
        (SVM, _("SVM")),
        (NAIVE_BAYES, _("Naive Bayes")),
        (GRADIENT_BOOSTING, _("Gradient Boosting")),
        (LINEAR_REGRESSION, _("Linear Regression")),
        (RIDGE_REGRESSION, _("Ridge Regression")),
        (LASSO_REGRESSION, _("Lasso Regression")),
        (MLP, _("MLP (Neural Network)")),
        (CNN, _("CNN")),
        (RNN, _("RNN")),
        (LSTM, _("LSTM")),
        (GRU, _("GRU")),
        (VOTING_CLASSIFIER, _("Voting Classifier")),
        (STACKING_CLASSIFIER, _("Stacking Classifier")),
        (BAGGING_CLASSIFIER, _("Bagging Classifier")),
        (ADABOOST, _("AdaBoost")),
        (ELO, _("ELO Rating")),
        (GLICKO, _("Glicko Rating")),
        (TRUESKILL, _("TrueSkill Rating")),
    )

    @classmethod
    def choices(cls):
        return cls.CHOICES


class ProblemTypeChoices:
    """Tipos de problemas de Machine Learning"""

    CLASSIFICATION = "classification"
    BINARY_CLASSIFICATION = "binary_classification"
    MULTICLASS_CLASSIFICATION = "multiclass_classification"
    REGRESSION = "regression"
    RATING = "rating"

    CHOICES = (
        (CLASSIFICATION, _("Classification")),
        (BINARY_CLASSIFICATION, _("Binary Classification")),
        (MULTICLASS_CLASSIFICATION, _("Multiclass Classification")),
        (REGRESSION, _("Regression")),
        (RATING, _("Rating System")),
    )

    @classmethod
    def choices(cls):
        return cls.CHOICES
