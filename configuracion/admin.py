from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    ConfiguracionHero,
    ConfiguracionSobreNosotros,
    ConfiguracionContacto,
    RedSocial,
)


# ============================================================
# HERO
# ============================================================

class ConfiguracionHeroForm(forms.ModelForm):

    class Meta:
        model = ConfiguracionHero
        fields = "__all__"

        widgets = {
            "overlay": forms.NumberInput(
                attrs={
                    "min": 0,
                    "max": 100,
                }
            ),
            "titulo": forms.TextInput(
                attrs={
                    "placeholder": (
                        "Cuidamos tu salud, cuidamos de ti."
                    )
                }
            ),
            "subtitulo": forms.Textarea(
                attrs={
                    "rows": 3,
                }
            ),
        }


@admin.register(ConfiguracionHero)
class ConfiguracionHeroAdmin(admin.ModelAdmin):

    form = ConfiguracionHeroForm

    list_display = (
        "fondo_preview",
        "archivo",
        "tipo",
        "overlay",
        "activo",
    )

    readonly_fields = (
        "fondo_preview",
        "archivo",
        "tipo",
    )

    fields = (
        "fondo",
        "fondo_preview",
        "archivo",
        "tipo",
        "titulo",
        "subtitulo",
        "overlay",
        "activo",
    )

    def has_add_permission(self, request):
        return not ConfiguracionHero.objects.exists()

    @admin.display(description="Archivo")
    def archivo(self, obj):
        return (
            obj.fondo.name
            if obj and obj.fondo
            else "Sin archivo"
        )

    @admin.display(description="Tipo")
    def tipo(self, obj):

        if not obj:
            return "—"

        if obj.es_video:
            return "Video"

        if obj.es_imagen:
            return "Imagen / GIF"

        return "No reconocido"

    @admin.display(description="Vista previa")
    def fondo_preview(self, obj):

        if not obj or not obj.fondo:
            return "Sin fondo"

        if obj.es_video:

            return format_html(
                '<video src="{}" muted controls '
                'style="width:320px;max-height:180px;'
                'object-fit:cover;border-radius:12px;"></video>',
                obj.fondo.url,
            )

        return format_html(
            '<img src="{}" '
            'style="width:320px;max-height:180px;'
            'object-fit:cover;border-radius:12px;" />',
            obj.fondo.url,
        )


# ============================================================
# SOBRE NOSOTROS
# ============================================================

@admin.register(ConfiguracionSobreNosotros)
class ConfiguracionSobreNosotrosAdmin(admin.ModelAdmin):

    fieldsets = (

        (
            "Contenido principal",
            {
                "fields": (
                    "etiqueta",
                    "titulo",
                    "parrafo_1",
                    "parrafo_2",
                )
            },
        ),

        (
            "Características",
            {
                "fields": (
                    "caracteristica_1_titulo",
                    "caracteristica_1_descripcion",
                    "caracteristica_2_titulo",
                    "caracteristica_2_descripcion",
                )
            },
        ),

        (
            "Tarjeta destacada",
            {
                "fields": (
                    "tarjeta_titulo",
                    "tarjeta_subtitulo",
                )
            },
        ),

        (
            "Estado",
            {
                "fields": (
                    "activo",
                )
            },
        ),

    )

    def has_add_permission(self, request):
        return not ConfiguracionSobreNosotros.objects.exists()


# ============================================================
# CONTACTO
# ============================================================

@admin.register(ConfiguracionContacto)
class ConfiguracionContactoAdmin(admin.ModelAdmin):

    fieldsets = (

        (
            "Contenido de la sección",
            {
                "fields": (
                    "titulo",
                    "descripcion",
                )
            },
        ),

        (
            "Teléfono y WhatsApp",
            {
                "fields": (
                    "telefono",
                    "whatsapp",
                )
            },
        ),

        (
            "Correo electrónico",
            {
                "fields": (
                    "email",
                )
            },
        ),

        (
            "Ubicación",
            {
                "fields": (
                    "direccion",
                    "mapa_url",
                )
            },
        ),

        (
            "Horario",
            {
                "fields": (
                    "horario",
                )
            },
        ),

        (
            "Estado",
            {
                "fields": (
                    "activo",
                )
            },
        ),

    )

    def has_add_permission(self, request):
        return not ConfiguracionContacto.objects.exists()


# ============================================================
# REDES SOCIALES
# ============================================================

@admin.register(RedSocial)
class RedSocialAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "icono",
        "url",
        "orden",
        "activo",
        "nueva_pestana",
    )

    list_filter = (
        "activo",
        "icono",
        "nueva_pestana",
    )

    search_fields = (
        "nombre",
        "url",
    )

    list_editable = (
        "orden",
        "activo",
    )

    ordering = (
        "orden",
        "id",
    )

    fields = (
        "nombre",
        "url",
        "icono",
        "orden",
        "activo",
        "nueva_pestana",
    )