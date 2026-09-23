from django.shortcuts import get_object_or_404, render

from .models import AreaServicio


# Create your views here.
def catalogo_servicios(request):

    areas = (
        AreaServicio.objects
        .filter(
            activo=True,
            servicios__activo=True
        )
        .prefetch_related("servicios")
        .distinct()
        .order_by("orden", "nombre")
    )

    return render(
        request,
        "servicios/catalogo.html",
        {
            "areas": areas,
        }
    )


def catalogo_area(request, slug):

    area = get_object_or_404(
        AreaServicio,
        slug=slug,
        activo=True
    )

    servicios = (
        area.servicios
        .filter(activo=True)
        .order_by("orden", "nombre")
    )

    return render(
        request,
        "servicios/catalogo.html",
        {
            "areas": [area],
            "area_seleccionada": area,
            "servicios": servicios,
        }
    )