"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from project_commands import views as tools_views
from predictions import views as predictions_views


def redirect_to_dashboard(request):
    return redirect("/dashboard/")


urlpatterns = [
    path("", redirect_to_dashboard, name="home"),
    path("admin/", admin.site.urls),
    path("dashboard/", include("dashboard.urls")),
    path("", include("django_prometheus.urls")),
    # Herramientas (management commands runner + SSE streaming)
    path("tools/", tools_views.tools_index, name="tools_index"),
    path(
        "tools/stream/",
        tools_views.tools_run_stream,
        name="tools_run_stream",
    ),
    # Visualización, Comparación y Global (stats)
    path(
        "visualization/",
        tools_views.visualization_index,
        name="visualization_index",
    ),
    path(
        "comparison/",
        tools_views.comparison_index,
        name="comparison_index",
    ),
    path("global/", tools_views.global_index, name="global_index"),
    # ML forecast
    path("ml/", tools_views.ml_forecast_index, name="ml_forecast_index"),
    # IA / Chat
    path("ia/", tools_views.ia_index, name="ia_index"),
    path("ia/ask/", tools_views.ia_ask, name="ia_ask"),
    # Prediction API endpoints
    path(
        "predict/matchup/",
        predictions_views.predict_matchup,
        name="predict_matchup",
    ),
    path(
        "predict/<str:game_id>/<str:market>/",
        predictions_views.predict,
        name="predict",
    ),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATICFILES_DIRS[0],
    )
