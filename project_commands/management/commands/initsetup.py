from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        created_superuser, error_superuser = self.create_superuser()
        created_manager, error_manager = self.create_manager_user()
        # created_groups, error_groups = self.create_groups_and_permissions()

        if not error_superuser:
            self.stdout.write(self.style.SUCCESS("Superuser created successfully ✅"))
        else:
            self.stdout.write(
                self.style.WARNING(f"Superuser already exists ❌ ({error_superuser})")
            )

        if not error_manager:
            self.stdout.write(
                self.style.SUCCESS("Manager user created successfully ✅")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Manager user already exists ❌ ({error_manager})")
            )

        # if not error_groups:
        #     self.stdout.write(self.style.SUCCESS("Groups created successfully ✅"))
        # else:
        #     self.stdout.write(self.style.WARNING(f"Groups already exist ❌ ({error_groups})"))

    def create_superuser(self):
        try:
            User = get_user_model()
            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    "admin",  # USERNAME
                    "admin@sanbox.org",  # MAIL
                    "admin",  # PASS
                )
                return True, None
            return False, "Usuario ya existe"
        except Exception as e:
            return False, str(e)

    def create_manager_user(self):
        try:
            User = get_user_model()

            with transaction.atomic():
                # Crear o obtener el usuario manager
                user, created = User.objects.get_or_create(
                    username="manager",
                    defaults={
                        "email": "manager@nba-data-manager.com",
                        "is_staff": True,
                        "is_superuser": False,
                    },
                )

                if not created:
                    # Asegurar que es staff pero no superuser
                    user.is_staff = True
                    user.is_superuser = False
                    user.email = "manager@nba-data-manager.com"
                    user.save()

                # Establecer contraseña
                user.set_password("manager123")
                user.save()

                # Obtener todos los permisos excepto los de Celery
                all_permissions = Permission.objects.all()

                # Filtrar permisos de Celery
                celery_apps = ["django_celery_beat", "django_celery_results"]
                manager_permissions = [
                    perm
                    for perm in all_permissions
                    if perm.content_type.app_label not in celery_apps
                ]

                # Asignar todos los permisos al usuario
                user.user_permissions.set(manager_permissions)

            if created:
                return True, None
            return False, "Usuario ya existe"
        except Exception as e:
            return False, str(e)

    def create_groups_and_permissions(self):
        try:
            for group in settings.ADMIN_GROUPS:
                Group.objects.get_or_create(name=group)

            role_permissions = settings.ROLE_PERMISSIONS

            for role_permission, permissions in role_permissions.items():
                role, created = Group.objects.get_or_create(name=role_permission)
                for item in permissions:
                    content_type = ContentType.objects.get(
                        app_label=item["app_label"], model=item["model"]
                    )
                    for permission in item["permissions"]:
                        # NOTE: If it exists, it is not added (there is no error)
                        role.permissions.add(
                            Permission.objects.get(
                                codename=f"{permission}_{item['model']}",
                                content_type=content_type,
                            )
                        )
            role.save()
            return True, None
        except Exception as e:
            return False, str(e)
