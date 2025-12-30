"""
Utilidades para exportar e importar modelos en CSV desde Django Admin
"""

import csv
from io import StringIO
from django.http import HttpResponse
from django.contrib import messages
from django.db import transaction, models


def export_as_csv(modeladmin, request, queryset):
    """
    Acción de admin para exportar los registros seleccionados a CSV
    """
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = (
        f"attachment; filename={meta.verbose_name_plural}.csv"
    )

    writer = csv.writer(response)
    writer.writerow(field_names)

    for obj in queryset:
        row = []
        for field in meta.fields:
            value = getattr(obj, field.name)
            # Manejar ForeignKey
            if hasattr(value, "__str__") and not isinstance(value, str):
                value = str(value)
            # Manejar valores None
            if value is None:
                value = ""
            row.append(value)
        writer.writerow(row)

    return response


export_as_csv.short_description = "Exportar seleccionados a CSV"


def import_from_csv(modeladmin, request, queryset):
    """
    Acción de admin para importar registros desde CSV
    Nota: Esta acción requiere que el usuario suba un archivo CSV.
    Para una implementación completa, se recomienda crear una vista personalizada.
    """
    messages.warning(
        request,
        "Para importar desde CSV, por favor use la funcionalidad de importación "
        "desde el comando de management o cree una vista personalizada.",
    )


import_from_csv.short_description = "Importar desde CSV (requiere vista personalizada)"


def get_csv_import_view(model_class):
    """
    Crea una función de vista para importar CSV para un modelo específico
    """

    def csv_import_view(request):
        if request.method == "POST" and request.FILES.get("csv_file"):
            csv_file = request.FILES["csv_file"]

            # Leer el archivo CSV
            decoded_file = csv_file.read().decode("utf-8")
            io_string = StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            meta = model_class._meta
            field_names = [field.name for field in meta.fields]

            created_count = 0
            updated_count = 0
            errors = []

            with transaction.atomic():
                for row_num, row in enumerate(
                    reader, start=2
                ):  # start=2 porque la fila 1 es el header
                    try:
                        # Preparar datos para crear/actualizar
                        data = {}
                        for field_name in field_names:
                            if field_name in row:
                                value = row[field_name].strip()

                                # Obtener el campo del modelo
                                field = meta.get_field(field_name)

                                # Manejar ForeignKey
                                if field.many_to_one:  # ForeignKey
                                    # Intentar encontrar el objeto relacionado
                                    related_model = field.related_model
                                    try:
                                        # Buscar por ID o por un campo único
                                        if value.isdigit():
                                            related_obj = related_model.objects.get(
                                                pk=int(value)
                                            )
                                        else:
                                            # Intentar buscar por el primer campo único o por __str__
                                            # Esto es genérico, puede necesitar ajustes específicos
                                            related_obj = related_model.objects.filter(
                                                **{related_model._meta.pk.name: value}
                                            ).first()
                                            if not related_obj:
                                                # Intentar por nombre si existe
                                                if hasattr(related_model, "name"):
                                                    related_obj = (
                                                        related_model.objects.filter(
                                                            name=value
                                                        ).first()
                                                    )

                                        if related_obj:
                                            data[field_name] = related_obj
                                        else:
                                            errors.append(
                                                f"Fila {row_num}: No se encontró el objeto relacionado para {field_name}={value}"
                                            )
                                            continue
                                    except Exception as e:
                                        errors.append(
                                            f"Fila {row_num}: Error al buscar {field_name}={value}: {str(e)}"
                                        )
                                        continue

                                # Manejar tipos de datos
                                elif isinstance(field, models.BooleanField):
                                    data[field_name] = value.lower() in (
                                        "true",
                                        "1",
                                        "yes",
                                        "sí",
                                        "si",
                                    )
                                elif isinstance(field, models.IntegerField):
                                    data[field_name] = int(value) if value else 0
                                elif isinstance(field, models.FloatField):
                                    data[field_name] = float(value) if value else 0.0
                                elif isinstance(field, models.DateTimeField):
                                    # Intentar parsear fecha
                                    from django.utils.dateparse import parse_datetime

                                    parsed = parse_datetime(value)
                                    if parsed:
                                        data[field_name] = parsed
                                elif isinstance(field, models.DateField):
                                    from django.utils.dateparse import parse_date

                                    parsed = parse_date(value)
                                    if parsed:
                                        data[field_name] = parsed
                                else:
                                    data[field_name] = value if value else ""

                        # Crear o actualizar el objeto
                        # Intentar encontrar un objeto existente por campos únicos
                        unique_fields = [
                            f for f in meta.fields if f.unique or f.primary_key
                        ]

                        if unique_fields:
                            # Buscar por el primer campo único
                            unique_field = unique_fields[0]
                            unique_value = data.get(unique_field.name)

                            if unique_value:
                                obj, created = model_class.objects.update_or_create(
                                    **{unique_field.name: unique_value}, defaults=data
                                )
                                if created:
                                    created_count += 1
                                else:
                                    updated_count += 1
                            else:
                                # Si no hay valor único, crear nuevo
                                model_class.objects.create(**data)
                                created_count += 1
                        else:
                            # Si no hay campos únicos, siempre crear nuevo
                            model_class.objects.create(**data)
                            created_count += 1

                    except Exception as e:
                        errors.append(f"Fila {row_num}: {str(e)}")
                        continue

            # Mensajes de resultado
            if created_count > 0:
                messages.success(
                    request, f"Se crearon {created_count} registros exitosamente."
                )
            if updated_count > 0:
                messages.success(
                    request, f"Se actualizaron {updated_count} registros exitosamente."
                )
            if errors:
                for error in errors[:10]:  # Mostrar solo los primeros 10 errores
                    messages.error(request, error)
                if len(errors) > 10:
                    messages.warning(
                        request,
                        f"Y {len(errors) - 10} errores más. Revise el archivo CSV.",
                    )

            return HttpResponse(
                f"Importación completada. Creados: {created_count}, Actualizados: {updated_count}, Errores: {len(errors)}"
            )

        return HttpResponse("Por favor, suba un archivo CSV válido.", status=400)

    return csv_import_view
