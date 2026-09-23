from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import models


class ConfiguracionHero(models.Model):
    """Configuración única del fondo del hero de la página principal."""

    fondo = models.FileField(
        upload_to="hero/",
        help_text="Imagen, GIF o video. Formatos: JPG, JPEG, PNG, WEBP, GIF, MP4 o WEBM.",
    )

    titulo = models.CharField(
        max_length=120,
        default="Cuidamos tu salud, cuidamos de ti.",
    )

    subtitulo = models.TextField(
        blank=True,
        default=(
            "Atención médica profesional, humana y cercana, porque tu bienestar "
            "y el de tu familia merecen lo mejor."
        ),
    )

    overlay = models.PositiveSmallIntegerField(
        default=75,
        help_text=(
            "Oscurecimiento del fondo para mejorar la lectura del texto "
            "(0 a 100%)."
        ),
    )

    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Configuración del Hero"
        verbose_name_plural = "Configuración del Hero"

    def __str__(self):
        return "Fondo del Hero"

    @property
    def extension(self):
        return (
            Path(self.fondo.name).suffix.lower().lstrip(".")
            if self.fondo
            else ""
        )

    @property
    def es_video(self):
        return self.extension in {
            "mp4",
            "webm",
            "ogg",
            "ogv",
        }

    @property
    def es_imagen(self):
        return self.extension in {
            "jpg",
            "jpeg",
            "png",
            "webp",
            "gif",
        }

    def clean(self):
        super().clean()

        if not self.fondo:
            raise ValidationError({
                "fondo": (
                    "Debes seleccionar un archivo para el fondo del hero."
                )
            })

        extension = self.extension

        permitidas = {
            "jpg",
            "jpeg",
            "png",
            "webp",
            "gif",
            "mp4",
            "webm",
            "ogg",
            "ogv",
        }

        if extension not in permitidas:
            raise ValidationError({
                "fondo": (
                    "Formato no permitido. Usa JPG, JPEG, PNG, WEBP, "
                    "GIF, MP4, WEBM u OGG."
                )
            })

        if not 0 <= self.overlay <= 100:
            raise ValidationError({
                "overlay": (
                    "El overlay debe estar entre 0 y 100."
                )
            })

    def save(self, *args, **kwargs):
        # Esta configuración es deliberadamente única.
        self.pk = 1
        self.activo = True
        self.full_clean()

        return super().save(*args, **kwargs)


class ConfiguracionSobreNosotros(models.Model):

    etiqueta = models.CharField(
        max_length=100,
        default="SOBRE NOSOTROS",
    )

    titulo = models.CharField(
        max_length=200,
        default="Una clínica comprometida con tu bienestar",
    )

    parrafo_1 = models.TextField(
        default=(
            "En Clínica Cruz Jiminian creemos que una buena atención médica "
            "comienza escuchando a nuestros pacientes."
        ),
    )

    parrafo_2 = models.TextField(
        default=(
            "Nuestro equipo trabaja para ofrecer servicios médicos de "
            "calidad en un ambiente profesional, seguro y humano."
        ),
    )

    caracteristica_1_titulo = models.CharField(
        max_length=100,
        default="Atención humana",
    )

    caracteristica_1_descripcion = models.CharField(
        max_length=200,
        default="Tratamos a cada paciente con respeto y empatía.",
    )

    caracteristica_2_titulo = models.CharField(
        max_length=100,
        default="Profesionales capacitados",
    )

    caracteristica_2_descripcion = models.CharField(
        max_length=200,
        default="Un equipo comprometido con tu salud.",
    )

    tarjeta_titulo = models.CharField(
        max_length=100,
        default="Compromiso",
    )

    tarjeta_subtitulo = models.CharField(
        max_length=150,
        default="con tu bienestar",
    )

    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Configuración de Sobre Nosotros"
        verbose_name_plural = "Configuración de Sobre Nosotros"

    def __str__(self):
        return "Sobre Nosotros"

    def save(self, *args, **kwargs):
        # Solo puede existir una configuración.
        self.pk = 1
        self.activo = True

        return super().save(*args, **kwargs)


# ============================================================
# CONFIGURACIÓN DE CONTACTO
# ============================================================

class ConfiguracionContacto(models.Model):

    titulo = models.CharField(
        max_length=150,
        default="Estamos aquí para ayudarte",
    )

    descripcion = models.TextField(
        blank=True,
        default=(
            "Ponte en contacto con nosotros para obtener más información "
            "sobre nuestros servicios."
        ),
    )

    telefono = models.CharField(
        max_length=50,
        blank=True,
        help_text="Ejemplo: 809-555-5555",
    )

    whatsapp = models.CharField(
        max_length=50,
        blank=True,
        help_text="Número de WhatsApp. Ejemplo: 8095555555",
    )

    email = models.EmailField(
        blank=True,
        help_text="Correo electrónico de contacto.",
    )

    direccion = models.CharField(
        max_length=250,
        blank=True,
        default="Santo Domingo, República Dominicana",
    )

    horario = models.CharField(
        max_length=200,
        blank=True,
        default="Lunes - Domingo",
    )

    mapa_url = models.URLField(
        blank=True,
        help_text="Enlace de Google Maps de la clínica.",
    )

    activo = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = "Configuración de Contacto"
        verbose_name_plural = "Configuración de Contacto"

    def __str__(self):
        return "Contacto"

    def save(self, *args, **kwargs):
        # Configuración única.
        self.pk = 1

        super().save(*args, **kwargs)


# ============================================================
# REDES SOCIALES
# ============================================================

class RedSocial(models.Model):

    ICONOS = [
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("tiktok", "TikTok"),
        ("youtube", "YouTube"),
        ("x", "X / Twitter"),
        ("linkedin", "LinkedIn"),
        ("whatsapp", "WhatsApp"),
        ("telegram", "Telegram"),
        ("globe", "Sitio web"),
    ]

    nombre = models.CharField(
        max_length=50,
        help_text="Nombre que aparecerá en el enlace.",
    )

    url = models.URLField(
        max_length=500,
        help_text="URL completa. Ejemplo: https://www.facebook.com/...",
    )

    icono = models.CharField(
        max_length=30,
        choices=ICONOS,
        default="globe",
    )

    orden = models.PositiveIntegerField(
        default=0,
        help_text="Menor número = aparece primero.",
    )

    activo = models.BooleanField(
        default=True,
    )

    nueva_pestana = models.BooleanField(
        default=True,
        verbose_name="Abrir en nueva pestaña",
    )

    class Meta:
        ordering = ["orden", "id"]
        verbose_name = "Red social"
        verbose_name_plural = "Redes sociales"

    def __str__(self):
        return self.nombre