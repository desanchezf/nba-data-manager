import os
import subprocess

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def dashboard_home(request):
    """Vista principal del dashboard con botones de acción"""
    context = {
        'title': 'NBA Data Manager Dashboard',
        'actions': [
            {
                'name': 'Importar Datos',
                'description': 'Importar datos de NBA desde fuentes externas',
                'url': 'dashboard:import_data',
                'icon': '📥',
                'color': 'primary'
            },
            {
                'name': 'Exportar Datos',
                'description': 'Exportar datos procesados a diferentes formatos',
                'url': 'dashboard:export_data',
                'icon': '📤',
                'color': 'success'
            },
            {
                'name': 'Limpiar Cache',
                'description': 'Limpiar cache del sistema para liberar memoria',
                'url': 'dashboard:clean_cache',
                'icon': '🧹',
                'color': 'warning'
            },
            {
                'name': 'Ejecutar Scraper',
                'description': 'Ejecutar el scraper para obtener datos actualizados',
                'url': 'dashboard:run_scraper',
                'icon': '🕷️',
                'color': 'info'
            },
            {
                'name': 'Panel de Admin',
                'description': 'Acceder al panel de administración de Django',
                'url': '/admin/',
                'icon': '⚙️',
                'color': 'secondary'
            }
        ]
    }
    return render(request, 'dashboard/home.html', context)


@require_POST
@csrf_exempt
def import_data_action(request):
    """Acción para importar datos"""
    try:
        # Aquí puedes agregar la lógica para importar datos
        # Por ejemplo, ejecutar comandos de Django management
        result = subprocess.run(
            ['python', 'manage.py', 'import'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        if result.returncode == 0:
            return JsonResponse({'status': 'success', 'message': 'Datos importados correctamente'})
        else:
            return JsonResponse({'status': 'error', 'message': f'Error al importar datos: {result.stderr}'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error inesperado: {str(e)}'})


@require_POST
@csrf_exempt
def export_data_action(request):
    """Acción para exportar datos"""
    try:
        # Lógica para exportar datos
        return JsonResponse({'status': 'success', 'message': 'Datos exportados correctamente'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error al exportar datos: {str(e)}'})


@require_POST
@csrf_exempt
def clean_cache_action(request):
    """Acción para limpiar cache"""
    try:
        cache.clear()
        return JsonResponse({'status': 'success', 'message': 'Cache limpiado correctamente'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error al limpiar cache: {str(e)}'})


@require_POST
@csrf_exempt
def run_scraper_action(request):
    """Acción para ejecutar scraper"""
    try:
        # Aquí puedes ejecutar el scraper específico
        # Por ejemplo, ejecutar uno de los scrapers del directorio scrapper/
        return JsonResponse({'status': 'success', 'message': 'Scraper ejecutado correctamente'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error al ejecutar scraper: {str(e)}'})
