from django.db import models


# Create your models here.
class AreaServicio(models.Model):
    nombre = models.CharField(
        max_length=150,
        unique=True
    )

    slug = models.SlugField(
        unique=True
    )

    descripcion = models.TextField(
        blank=True
    )

    icono = models.CharField(
        max_length=50,
        blank=True,
        help_text="Clase, emoji o identificador del icono"
    )

    imagen = models.ImageField(
        upload_to="areas_servicios/",
        blank=True,
        null=True
    )

    activo = models.BooleanField(
        default=True
    )

    destacado = models.BooleanField(
        default=False,
        help_text="Mostrar esta área como tarjeta en la página de inicio."
    )

    orden = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "Área de servicio"
        verbose_name_plural = "Áreas de servicios"

    def __str__(self):
        return self.nombre


class Servicio(models.Model):

    area = models.ForeignKey(
        AreaServicio,
        on_delete=models.CASCADE,
        related_name="servicios",
        null=True,
        blank=True
    )

    nombre = models.CharField(
        max_length=150
    )

    slug = models.SlugField(
        unique=True
    )

    descripcion = models.TextField()

    icono = models.CharField(
        max_length=50,
        blank=True,
        help_text="Clase o identificador del icono"
    )

    preparacion = models.TextField(
        blank=True,
        help_text="Indicaciones que debe seguir el paciente antes del estudio."
    )

    duracion = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ejemplo: 20-30 minutos"
    )

    requiere_cita = models.BooleanField(
        default=True
    )

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    activo = models.BooleanField(
        default=True
    )

    orden = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return self.nombre


class ConfiguracionSitio(models.Model):

    nombre_clinica = models.CharField(
        max_length=150,
        default="Clínica Cruz Jiminian"
    )

    logo_header = models.ImageField(
        upload_to="logos/",
        blank=True,
        null=True
    )

    activo = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = "Configuración del sitio"
        verbose_name_plural = "Configuración del sitio"

    def __str__(self):
        return self.nombre_clinica