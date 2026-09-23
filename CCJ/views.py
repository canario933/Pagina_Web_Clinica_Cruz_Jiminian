from django.shortcuts import render

from servicios.models import AreaServicio
from medicos.models import Medico, FotoSobreNosotros
from configuracion.models import ConfiguracionHero


def inicio(request):

    areas_servicios = (
        AreaServicio.objects
        .filter(
            activo=True,
            destacado=True
        )
        .prefetch_related(
            "servicios"
        )
        .order_by(
            "orden",
            "nombre"
        )
    )

    medicos_destacados = list(
        Medico.objects
        .filter(
            activo=True,
            destacado=True
        )
        .select_related("especialidad")
        .order_by(
            "orden_destacado",
            "apellido",
            "nombre"
        )[:4]
    )

    # Mientras se configuran los destacados,
    # la página no queda vacía.
    if not medicos_destacados:

        medicos_destacados = list(
            Medico.objects
            .filter(activo=True)
            .select_related("especialidad")
            .order_by(
                "apellido",
                "nombre"
            )[:4]
        )

    medicos = (
        Medico.objects
        .filter(activo=True)
        .select_related("especialidad")
    )

    fotos_sobre_nosotros = (
        FotoSobreNosotros.objects
        .filter(activo=True)
    )

    hero = (
        ConfiguracionHero.objects
        .filter(activo=True)
        .first()
    )

    context = {

        "areas_servicios": areas_servicios,

        "medicos": medicos,

        "medicos_destacados": medicos_destacados,

        "fotos_sobre_nosotros": fotos_sobre_nosotros,

        "hero": hero,

    }

    return render(
        request,
        "inicio.html",
        context
    )