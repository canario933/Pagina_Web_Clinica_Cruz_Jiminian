from django.urls import path

from . import views


urlpatterns = [
    path(
        "reservar/",
        views.reservar_cita,
        name="reservar_cita"
    ),

    path(
        "api/fechas/<int:medico_id>/",
        views.fechas_disponibles,
        name="fechas_disponibles"
    ),

    path(
        "api/horas/<int:medico_id>/",
        views.horas_disponibles,
        name="horas_disponibles"
    ),
]