from django.db import models
from django.utils.text import slugify

# Create your models here.
class Especialidad(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"

    def __str__(self):
        return self.nombre


class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    slug = models.SlugField(
        max_length=180,
        blank=True
    )

    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
        related_name="medicos"
    )

    foto = models.ImageField(
        upload_to="medicos/",
        blank=True,
        null=True
    )

    descripcion = models.TextField(blank=True)
    destacado = models.BooleanField(
        default=False,
        help_text="Mostrar este médico entre los destacados en la página principal."
    )
    orden_destacado = models.PositiveIntegerField(
        default=0,
        help_text="Menor número = mayor prioridad entre los destacados."
    )
    matricula = models.CharField(
        max_length=100,
        blank=True
    )

    activo = models.BooleanField(default=True)

    servicios = models.ManyToManyField(
        "servicios.Servicio",
        blank=True,
        related_name="medicos",
        verbose_name="Servicios que realiza",
    )
    
    class Meta:
        ordering = ["apellido", "nombre"]
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.nombre} {self.apellido}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dr. {self.nombre} {self.apellido}"

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

class FotoSobreNosotros(models.Model):
    imagen = models.ImageField(upload_to="sobre_nosotros/")
    texto_alternativo = models.CharField(max_length=180, blank=True)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "id"]
        verbose_name = "Foto de Sobre Nosotros"
        verbose_name_plural = "Fotos de Sobre Nosotros"

    def __str__(self):
        return self.texto_alternativo or f"Foto {self.pk}"
