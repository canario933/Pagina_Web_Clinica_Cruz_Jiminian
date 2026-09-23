from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views

urlpatterns = [
    path(
        "admin/", 
        admin.site.urls
    ),

    path(
        "", 
        views.inicio, 
        name="inicio"
    ),

    path(
        "citas/", 
        include("citas.urls")
    ),

    path(
        "medicos/", 
        include("medicos.urls")
    ),

    path(
        "servicios/", 
        include("servicios.urls")
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
