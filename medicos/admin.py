from django.contrib import admin
from django.utils.html import format_html

from citas.models import HorarioMedico
from .models import Especialidad, Medico, FotoSobreNosotros
from .forms import HorarioMedicoForm

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)


class HorarioMedicoInline(admin.TabularInline):
    model = HorarioMedico
    form = HorarioMedicoForm
    extra = 1
    
    fields = (
        "dia_semana",
        "hora_inicio",
        "hora_fin",
        "intervalo_minutos",
        "activo",
    )
    ordering = ("dia_semana", "hora_inicio")


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "apellido",
        "especialidad",
        "destacado",
        "orden_destacado",
        "foto_preview",
        "activo",
    )
    list_filter = ("especialidad", "destacado", "activo")
    search_fields = ("nombre", "apellido", "matricula")
    autocomplete_fields = ("especialidad",)
    filter_horizontal = ("servicios",)
    inlines = (HorarioMedicoInline,)

    readonly_fields = ("foto_preview",)

    @admin.display(description="Vista previa")
    def foto_preview(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" style="width:80px;height:80px;object-fit:cover;border-radius:12px;" />',
                obj.foto.url,
            )
        return "Sin foto"

    fieldsets = (
        ("Información del médico", {
            "fields": ("nombre", "apellido", "especialidad", "servicios", "foto", "foto_preview", "descripcion", "matricula")
        }),
        ("Página principal", {
            "fields": ("destacado", "orden_destacado", "activo")
        }),
    )


@admin.register(FotoSobreNosotros)
class FotoSobreNosotrosAdmin(admin.ModelAdmin):
    list_display = ("orden", "imagen_preview", "texto_alternativo", "activo")
    list_filter = ("activo",)
    ordering = ("orden", "id")

    @admin.display(description="Vista previa")
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="width:90px;height:60px;object-fit:cover;border-radius:10px;" />',
                obj.imagen.url,
            )
        return "Sin imagen"
