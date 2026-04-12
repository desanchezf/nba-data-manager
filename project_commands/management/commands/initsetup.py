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

        ok, msg = self.setup_ollama()
        if ok:
            self.stdout.write(self.style.SUCCESS(f"Ollama setup: {msg} ✅"))
        else:
            self.stdout.write(self.style.WARNING(f"Ollama setup: {msg}"))

        ok, msg = self.setup_system_prompt()
        if ok:
            self.stdout.write(self.style.SUCCESS(f"System prompt: {msg} ✅"))
        else:
            self.stdout.write(self.style.WARNING(f"System prompt: {msg}"))

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

    def setup_ollama(self):
        try:
            from ia.models import OllamaModelConfig, OllamaServer
            from ia.ollama_defaults import get_default_ollama_model_specs

            base_url = getattr(settings, "OLLAMA_BASE_URL", "http://localhost:11434")
            server, created = OllamaServer.objects.get_or_create(
                name="Local Ollama",
                defaults={"base_url": base_url, "enabled": True},
            )

            specs = get_default_ollama_model_specs()
            count = 0
            for spec in specs:
                _, mc = OllamaModelConfig.objects.get_or_create(
                    server=server,
                    model_name=spec["model_name"],
                    defaults={
                        "purpose": spec.get("purpose", "general"),
                        "context_tokens": spec.get("context_tokens", 4096),
                        "is_default": spec.get("is_default", False),
                        "enabled": True,
                    },
                )
                if mc:
                    count += 1

            return True, f"{'creado' if created else 'existente'}, {count} modelos configurados"
        except Exception as exc:
            return False, str(exc)

    def setup_system_prompt(self):
        try:
            from ia.models import SystemPrompt

            nba_prompt = (
                "Eres un asistente experto en análisis de baloncesto NBA. "
                "Tienes acceso a estadísticas de equipos y jugadores, métricas avanzadas "
                "(eFG%, TS%, PER, ORTG, DRTG), y modelos de predicción para mercados de "
                "apuestas (moneyline, totales, spreads). "
                "Ayuda a analizar partidos, interpretar features del modelo XGBoost, "
                "identificar valor en cuotas y evaluar el rendimiento histórico del modelo. "
                "Responde siempre en español y de forma concisa. "
                "Cuando des probabilidades o picks, indica siempre el nivel de confianza "
                "y el contexto (forma reciente, H2H, lesiones si las conoces)."
            )

            _, created = SystemPrompt.objects.get_or_create(
                name="NBA Assistant",
                defaults={
                    "content": nba_prompt,
                    "is_active": True,
                },
            )
            return True, "creado" if created else "ya existía"
        except Exception as exc:
            return False, str(exc)

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
