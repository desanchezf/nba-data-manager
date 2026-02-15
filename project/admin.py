from django.contrib import admin
from django.contrib.admin.apps import AdminConfig


class NBAAdminSite(admin.AdminSite):
    """
    AdminSite personalizado que oculta las apps de Celery
    para usuarios que no sean superuser
    """

    def get_app_list(self, request):
        """
        Retorna la lista de apps, ocultando Celery para usuarios no superuser
        """
        app_list = super().get_app_list(request)

        # Si el usuario no es superuser, ocultar apps de Celery
        if not request.user.is_superuser:
            app_list = [
                app for app in app_list
                if app['app_label'] not in ['django_celery_beat', 'django_celery_results']
            ]

        return app_list


class NBAAdminConfig(AdminConfig):
    default_site = 'project.admin.NBAAdminSite'
