from django.contrib import admin

from .models import (
    AreaServicio,
    Servicio,
    ConfiguracionSitio,
)


# Register your models here.
@admin.register(AreaServicio)
class AreaServicioAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "destacado",
        "activo",
        "orden",
    )

    list_filter = (
        "destacado",
        "activo",
    )

    search_fields = (
        "nombre",
        "descripcion",
    )

    prepopulated_fields = {
        "slug": ("nombre",)
    }

    ordering = (
        "orden",
        "nombre",
    )

    list_editable = (
        "destacado",
        "activo",
        "orden",
    )


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "area",
        "activo",
        "orden",
    )

    list_filter = (
        "activo",
        "area",
        "requiere_cita",
    )

    search_fields = (
        "nombre",
        "descripcion",
        "preparacion",
    )

    prepopulated_fields = {
        "slug": ("nombre",)
    }

    ordering = (
        "area",
        "orden",
        "nombre",
    )


@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):

    list_display = (
        "nombre_clinica",
        "activo",
        "logo_header",
    )

    fields = (
        "nombre_clinica",
        "logo_header",
        "activo",
    )

    def has_add_permission(self, request):
        return not ConfiguracionSitio.objects.exists()