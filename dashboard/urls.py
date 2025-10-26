from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('action/import-data/', views.import_data_action, name='import_data'),
    path('action/export-data/', views.export_data_action, name='export_data'),
    path('action/clean-cache/', views.clean_cache_action, name='clean_cache'),
    path('action/run-scraper/', views.run_scraper_action, name='run_scraper'),
]
