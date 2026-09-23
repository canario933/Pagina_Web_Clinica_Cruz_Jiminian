from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from django.db.models import Q
from medicos.models import Medico

# Create your models here.
class HorarioMedico(models.Model):

    DIAS_SEMANA = [
        (0, "Lunes"),
        (1, "Martes"),
        (2, "Miércoles"),
        (3, "Jueves"),
        (4, "Viernes"),
        (5, "Sábado"),
        (6, "Domingo"),
    ]

    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name="horarios"
    )

    dia_semana = models.PositiveSmallIntegerField(
        choices=DIAS_SEMANA
    )

    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    intervalo_minutos = models.PositiveIntegerField(
        default=30,
        help_text="Duración de cada espacio disponible."
    )

    activo = models.BooleanField(default=True)

    def clean(self):
        if self.hora_inicio >= self.hora_fin:
            raise ValidationError(
                {"hora_fin": "La hora de fin debe ser posterior a la hora de inicio."}
            )

        if self.intervalo_minutos <= 0:
            raise ValidationError(
                {"intervalo_minutos": "El intervalo debe ser mayor que 0 minutos."}
            )

    class Meta:
        ordering = ["dia_semana", "hora_inicio"]
        verbose_name = "Horario médico"
        verbose_name_plural = "Horarios médicos"

    def __str__(self):
        return (
            f"{self.medico} - "
            f"{self.get_dia_semana_display()} "
            f"{self.hora_inicio} - {self.hora_fin}"
        )

class Cita(models.Model):

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"),
        ("cancelada", "Cancelada"),
        ("completada", "Completada"),
    ]

    numero_cita = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        blank=True,
    )

    medico = models.ForeignKey(
        Medico,
        on_delete=models.PROTECT,
        related_name="citas"
    )

    paciente_nombre = models.CharField(max_length=100)
    paciente_apellido = models.CharField(max_length=100)

    telefono = models.CharField(max_length=30)
    email = models.EmailField(blank=True)

    fecha = models.DateField()
    hora = models.TimeField()

    motivo = models.TextField(blank=True)

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente"
    )

    creado_en = models.DateTimeField(
        auto_now_add=True
    )

    actualizado_en = models.DateTimeField(
        auto_now=True
    )

    def clean(self):
        if self.fecha and self.fecha < timezone.localdate():
            raise ValidationError(
                {"fecha": "La fecha de la cita no puede ser anterior a hoy."}
            )

        if self.medico_id and self.fecha and self.hora:
            if not HorarioMedico.objects.filter(
                medico_id=self.medico_id,
                dia_semana=self.fecha.weekday(),
                activo=True,
                hora_inicio__lte=self.hora,
                hora_fin__gt=self.hora,
            ).exists():
                raise ValidationError(
                    "El médico no tiene disponibilidad para esa fecha y hora."
                )

    def save(self, *args, **kwargs):
        if not self.numero_cita:
            super().save(*args, **kwargs)

            self.numero_cita = (
                f"CCJ-{self.creado_en.year}-{self.id:06d}"
            )

            super().save(
                update_fields=["numero_cita"]
            )
            return

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-fecha", "-hora"]
        verbose_name = "Cita"
        verbose_name_plural = "Citas"

        constraints = [
            models.UniqueConstraint(
                fields=["medico", "fecha", "hora"],
                condition=Q(
                    estado__in=["pendiente", "confirmada"]
                ),
                name="cita_medico_fecha_hora_activa_unica",
            )
        ]

    def __str__(self):
        return (
            f"{self.fecha} {self.hora} - "
            f"{self.medico} - "
            f"{self.paciente_nombre} {self.paciente_apellido}"
        )