from configuracion.models import (
    ConfiguracionContacto,
    RedSocial,
)

from .models import ConfiguracionSitio


def configuracion_sitio(request):

    return {
        "configuracion": (
            ConfiguracionSitio.objects
            .filter(activo=True)
            .first()
        ),

        "contacto": (
            ConfiguracionContacto.objects
            .filter(activo=True)
            .first()
        ),

        "redes_sociales": (
            RedSocial.objects
            .filter(activo=True)
            .order_by("orden", "id")
        ),
    }