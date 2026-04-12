import os

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

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


# ──────────────────────────────────────────────────────────────────────────────
# Ollama / LLM Chat models
# ──────────────────────────────────────────────────────────────────────────────

class SystemPrompt(models.Model):
    """
    Prompt de sistema enviado a todos los LLMs como contexto inicial.
    Solo puede haber un prompt activo al mismo tiempo.
    """

    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    content = models.TextField(verbose_name="Contenido del prompt")
    is_active = models.BooleanField(
        default=False,
        verbose_name="Activo",
        help_text="Solo un prompt puede estar activo. Al activar este se desactivan los demás.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Prompt de sistema"
        verbose_name_plural = "Prompts de sistema"
        ordering = ["-is_active", "-updated_at"]

    def __str__(self):
        status = "✓ activo" if self.is_active else "inactivo"
        return f"{self.name} ({status})"

    def save(self, *args, **kwargs):
        if self.is_active:
            SystemPrompt.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_active(cls):
        return cls.objects.filter(is_active=True).first()


class OllamaServer(models.Model):
    """Configuración de un servidor Ollama."""

    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField(
        help_text="URL base del servidor Ollama, p.ej. http://localhost:11434",
    )
    enabled = models.BooleanField(default=True)
    api_key = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Servidor Ollama"
        verbose_name_plural = "Servidores Ollama"

    def __str__(self):
        return self.name


class OllamaModelConfig(models.Model):
    """Configuración de un modelo concreto servido vía Ollama."""

    server = models.ForeignKey(OllamaServer, on_delete=models.CASCADE, related_name="models")
    model_name = models.CharField(max_length=100)
    temperature = models.FloatField(default=0.7)
    top_p = models.FloatField(default=0.9)
    max_tokens = models.PositiveIntegerField(default=512)
    alias = models.CharField(max_length=100, help_text="Nombre lógico en la app")
    description = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    deprecated = models.BooleanField(default=False)
    deprecated_at = models.DateTimeField(null=True, blank=True)

    # Estado de sincronización con Ollama
    ollama_sync_at = models.DateTimeField(null=True, blank=True, verbose_name="Última comprobación")
    ollama_installed = models.BooleanField(null=True, blank=True, verbose_name="Instalado en Ollama")
    ollama_local_digest = models.CharField(max_length=128, blank=True, verbose_name="Digest local")
    ollama_registry_digest = models.CharField(max_length=128, blank=True, verbose_name="Digest en registry")
    ollama_up_to_date = models.BooleanField(null=True, blank=True, verbose_name="Al día")
    ollama_sync_detail = models.CharField(max_length=500, blank=True, verbose_name="Detalle sincronización")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Modelo Ollama"
        verbose_name_plural = "Modelos Ollama"
        unique_together = ("server", "model_name")

    @property
    def is_deprecated(self):
        return self.deprecated or self.deprecated_at is not None

    def __str__(self):
        return f"{self.alias} ({self.server.name}:{self.model_name})"


class ChatSession(models.Model):
    """Sesión de conversación con un modelo Ollama."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ia_chat_sessions",
    )
    model_key = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sesión de chat"
        verbose_name_plural = "Sesiones de chat"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Sesión {self.pk} ({self.user}, {self.updated_at})"


class ChatMessage(models.Model):
    """Mensaje dentro de una sesión de chat (usuario o asistente)."""

    ROLE_USER = "user"
    ROLE_ASSISTANT = "assistant"
    ROLE_CHOICES = [(ROLE_USER, "Usuario"), (ROLE_ASSISTANT, "Asistente")]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mensaje de chat"
        verbose_name_plural = "Mensajes de chat"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
