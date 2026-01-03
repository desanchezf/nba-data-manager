from django.db import models
from django.core.validators import FileExtensionValidator
import os
from ia.enums import AlgorithmChoices, ProblemTypeChoices


def model_file_path(instance, filename):
    """Genera la ruta para guardar el archivo del modelo"""
    # Guarda en: ml/models/{model_name}/{filename}
    return os.path.join("ml", "models", instance.name, filename)


class PredictionModel(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    algorithm_type = models.CharField(
        max_length=50, choices=AlgorithmChoices.choices(), blank=True
    )
    problem_type = models.CharField(
        max_length=50, choices=ProblemTypeChoices.choices(), blank=True
    )
    model_file = models.FileField(
        upload_to=model_file_path,
        validators=[FileExtensionValidator(allowed_extensions=["pkl"])],
        blank=True,
        null=True,
        help_text="Archivo .pkl del modelo entrenado",
    )
    version = models.CharField(max_length=50, default="1.0.0")
    is_active = models.BooleanField(
        default=True, help_text="Modelo activo para predicciones"
    )
    metrics = models.JSONField(
        default=dict,
        blank=True,
        help_text=("Métricas de evaluación del modelo (accuracy, mse, r2, etc.)"),
    )
    training_data_info = models.JSONField(
        default=dict,
        blank=True,
        help_text=(
            "Información sobre los datos de entrenamiento (tamaño, features, etc.)"
        ),
    )
    hyperparameters = models.JSONField(
        default=dict,
        blank=True,
        help_text="Hiperparámetros del modelo",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trained_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Prediction Model"
        verbose_name_plural = "Prediction Models"

    def __str__(self):
        return f"{self.name} ({self.algorithm_type or 'N/A'})"

    def delete(self, *args, **kwargs):
        """Elimina el archivo del modelo cuando se elimina el registro"""
        if self.model_file:
            if os.path.isfile(self.model_file.path):
                os.remove(self.model_file.path)
        super().delete(*args, **kwargs)
