from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET

from medicos.models import Medico

from .models import Cita, HorarioMedico


ESTADOS_QUE_BLOQUEAN = ("pendiente", "confirmada")
DIAS_A_MOSTRAR = 60
DIAS_NOMBRES = [
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
    "Domingo",
]

def _volver_a_citas():
    return redirect(reverse("inicio") + "#citas")


def _espacios_del_horario(horario, fecha):
    inicio = datetime.combine(fecha, horario.hora_inicio)
    fin = datetime.combine(fecha, horario.hora_fin)

    if horario.intervalo_minutos <= 0 or inicio >= fin:
        return []

    espacios = []
    actual = inicio
    intervalo = timedelta(minutes=horario.intervalo_minutos)

    while actual + intervalo <= fin:
        espacios.append(actual.time())
        actual += intervalo

    return espacios

def obtener_horas_disponibles(medico, fecha):
    """Calcula los espacios libres según el horario semanal del médico."""
    if fecha < timezone.localdate():
        return []

    horarios = HorarioMedico.objects.filter(
        medico=medico,
        dia_semana=fecha.weekday(),
        activo=True,
    ).order_by("hora_inicio")

    horas = []
    for horario in horarios:
        horas.extend(_espacios_del_horario(horario, fecha))

    ocupadas = set(
        Cita.objects.filter(
            medico=medico,
            fecha=fecha,
            estado__in=ESTADOS_QUE_BLOQUEAN,
        ).values_list("hora", flat=True)
    )

    ahora = timezone.localtime()
    if fecha == ahora.date():
        horas = [hora for hora in horas if hora > ahora.time()]

    return sorted(set(horas) - ocupadas)


@require_GET
def fechas_disponibles(request, medico_id):
    try:
        medico = Medico.objects.get(id=medico_id, activo=True)
    except Medico.DoesNotExist:
        return JsonResponse({"fechas": [], "error": "Médico no encontrado."}, status=404)

    hoy = timezone.localdate()
    fechas = []

    for offset in range(DIAS_A_MOSTRAR):
        fecha = hoy + timedelta(days=offset)
        if obtener_horas_disponibles(medico, fecha):
            fechas.append({
                "fecha": fecha.isoformat(),
                "texto": fecha.strftime("%d/%m/%Y"),
                "dia": DIAS_NOMBRES[fecha.weekday()],
            })

    return JsonResponse({"fechas": fechas})


@require_GET
def horas_disponibles(request, medico_id):
    fecha_str = request.GET.get("fecha", "")

    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return JsonResponse({"horas": [], "error": "Fecha inválida."}, status=400)

    try:
        medico = Medico.objects.get(id=medico_id, activo=True)
    except Medico.DoesNotExist:
        return JsonResponse({"horas": [], "error": "Médico no encontrado."}, status=404)

    horas = obtener_horas_disponibles(medico, fecha)

    return JsonResponse({
        "horas": [hora.strftime("%H:%M") for hora in horas],
        "mensaje": (
            "No hay horas disponibles para esta fecha."
            if not horas
            else ""
        ),
    })


def reservar_cita(request):
    if request.method != "POST":
        return _volver_a_citas()

    medico_id = request.POST.get("medico")
    fecha_str = request.POST.get("fecha")
    hora_str = request.POST.get("hora")

    try:
        medico = Medico.objects.get(id=medico_id, activo=True)
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        hora = datetime.strptime(hora_str, "%H:%M").time()
    except (Medico.DoesNotExist, TypeError, ValueError):
        messages.error(request, "Los datos de la cita no son válidos.")
        return _volver_a_citas()

    if fecha < timezone.localdate():
        messages.error(request, "No puedes reservar una fecha pasada.")
        return _volver_a_citas()

    if hora not in obtener_horas_disponibles(medico, fecha):
        messages.error(request, "La fecha u hora seleccionada ya no está disponible.")
        return _volver_a_citas()

    datos = {
        "medico": medico,
        "paciente_nombre": request.POST.get("paciente_nombre", "").strip(),
        "paciente_apellido": request.POST.get("paciente_apellido", "").strip(),
        "telefono": request.POST.get("telefono", "").strip(),
        "email": request.POST.get("email", "").strip(),
        "fecha": fecha,
        "hora": hora,
        "motivo": request.POST.get("motivo", "").strip(),
        "estado": "pendiente",
    }

    if not datos["paciente_nombre"] or not datos["paciente_apellido"] or not datos["telefono"]:
        messages.error(request, "Completa nombre, apellido y teléfono.")
        return _volver_a_citas()

    try:
        with transaction.atomic():
            cita = Cita.objects.create(**datos)
    except IntegrityError:
        messages.error(
            request,
            "Ese horario acaba de ser reservado. Selecciona otra hora.",
        )
        return _volver_a_citas()

    return render(
        request,
        "citas/confirmacion.html",
        {
            "cita": cita,
        },
    )
