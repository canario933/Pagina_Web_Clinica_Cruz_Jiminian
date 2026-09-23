from django.contrib import admin

from .models import HorarioMedico, Cita


@admin.register(HorarioMedico)
class HorarioMedicoAdmin(admin.ModelAdmin):
    list_display = (
        "medico",
        "dia_semana",
        "hora_inicio",
        "hora_fin",
        "intervalo_minutos",
        "activo",
    )
    list_filter = ("dia_semana", "activo")
    search_fields = ("medico__nombre", "medico__apellido")
    autocomplete_fields = ("medico",)


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = (
        "numero_cita",
        "paciente_nombre",
        "paciente_apellido",
        "medico",
        "fecha",
        "hora",
        "estado",
        "creado_en",
    )

    list_filter = (
        "estado",
        "medico",
        "fecha",
    )

    search_fields = (
        "numero_cita",
        "paciente_nombre",
        "paciente_apellido",
        "telefono",
        "email",
    )

    autocomplete_fields = (
        "medico",
    )

    readonly_fields = (
        "numero_cita",
        "creado_en",
        "actualizado_en",
    )

    date_hierarchy = "fecha"

    ordering = (
        "-fecha",
        "-hora",
    )

    actions = (
        "confirmar_citas",
        "cancelar_citas",
        "completar_citas",
    )

    fieldsets = (
        (
            "Información de la cita",
            {
                "fields": (
                    "numero_cita",
                    "medico",
                    "fecha",
                    "hora",
                    "estado",
                )
            },
        ),
        (
            "Información del paciente",
            {
                "fields": (
                    "paciente_nombre",
                    "paciente_apellido",
                    "telefono",
                    "email",
                )
            },
        ),
        (
            "Motivo de la consulta",
            {
                "fields": (
                    "motivo",
                )
            },
        ),
        (
            "Información del sistema",
            {
                "fields": (
                    "creado_en",
                    "actualizado_en",
                )
            },
        ),
    )

    @admin.action(description="Confirmar citas seleccionadas")
    def confirmar_citas(modeladmin, request, queryset):
        queryset.update(estado="confirmada")

    @admin.action(description="Cancelar citas seleccionadas")
    def cancelar_citas(modeladmin, request, queryset):
        queryset.update(estado="cancelada")

    @admin.action(description="Marcar como completadas")
    def completar_citas(modeladmin, request, queryset):
        queryset.update(estado="completada")