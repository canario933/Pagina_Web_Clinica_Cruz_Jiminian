from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.catalogo_medicos,
        name="catalogo_medicos"
    ),

    path(
        "<slug:slug>/",
        views.detalle_medico,
        name="detalle_medico"
    ),
]