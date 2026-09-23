from django.shortcuts import render, get_object_or_404

from .models import Especialidad, Medico


def catalogo_medicos(request):
    especialidades = (
        Especialidad.objects.filter(activo=True)
        .prefetch_related("medicos")
        .order_by("nombre")
    )

    medicos = (
        Medico.objects.filter(activo=True)
        .select_related("especialidad")
        .order_by("especialidad__nombre", "apellido", "nombre")
    )

    return render(request, "medicos/catalogo.html", {
        "especialidades": especialidades,
        "medicos": medicos,
    })

def detalle_medico(request, slug):
    medico = get_object_or_404(
        Medico.objects
        .select_related("especialidad")
        .prefetch_related("servicios"),
        slug=slug,
        activo=True,
    )

    horarios = (
        medico.horarios
        .filter(activo=True)
        .order_by("dia_semana", "hora_inicio")
    )

    servicios = medico.servicios.filter(activo=True)

    return render(
        request,
        "medicos/detalle.html",
        {
            "medico": medico,
            "horarios": horarios,
            "servicios": servicios,
        },
    )