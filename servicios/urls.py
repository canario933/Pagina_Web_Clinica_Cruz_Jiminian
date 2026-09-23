from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.catalogo_servicios,
        name="catalogo_servicios"
    ),

    path(
        "<slug:slug>/",
        views.catalogo_area,
        name="catalogo_area"
    ),
]