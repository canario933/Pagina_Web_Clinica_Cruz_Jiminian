from django import forms

from citas.models import HorarioMedico


def generar_horas():
    horas = []

    for hora in range(24):
        for minuto in (0, 30):
            valor = f"{hora:02d}:{minuto:02d}"

            # Convertir a formato de 12 horas
            if hora == 0:
                hora_12 = 12
                periodo = "AM"
            elif hora < 12:
                hora_12 = hora
                periodo = "AM"
            elif hora == 12:
                hora_12 = 12
                periodo = "PM"
            else:
                hora_12 = hora - 12
                periodo = "PM"

            etiqueta = f"{hora_12:02d}:{minuto:02d} {periodo}"

            horas.append((valor, etiqueta))

    return horas


class HorarioMedicoForm(forms.ModelForm):

    class Meta:
        model = HorarioMedico
        fields = "__all__"
        widgets = {
            "hora_inicio": forms.Select(
                choices=generar_horas()
            ),
            "hora_fin": forms.Select(
                choices=generar_horas()
            ),
        }