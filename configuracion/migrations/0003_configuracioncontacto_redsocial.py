from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("configuracion", "0002_configuracionsobrenosotros"),
    ]

    operations = [

        migrations.CreateModel(
            name="ConfiguracionContacto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),

                (
                    "titulo",
                    models.CharField(
                        default="Estamos aquí para ayudarte",
                        max_length=150,
                    ),
                ),

                (
                    "descripcion",
                    models.TextField(
                        blank=True,
                        default=(
                            "Ponte en contacto con nosotros para obtener "
                            "más información sobre nuestros servicios."
                        ),
                    ),
                ),

                (
                    "telefono",
                    models.CharField(
                        blank=True,
                        help_text="Ejemplo: 809-555-5555",
                        max_length=50,
                    ),
                ),

                (
                    "whatsapp",
                    models.CharField(
                        blank=True,
                        help_text="Número de WhatsApp. Ejemplo: 8095555555",
                        max_length=50,
                    ),
                ),

                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        help_text="Correo electrónico de contacto.",
                    ),
                ),

                (
                    "direccion",
                    models.CharField(
                        default="Santo Domingo, República Dominicana",
                        blank=True,
                        max_length=250,
                    ),
                ),

                (
                    "horario",
                    models.CharField(
                        default="Lunes - Domingo",
                        blank=True,
                        max_length=200,
                    ),
                ),

                (
                    "mapa_url",
                    models.URLField(
                        blank=True,
                        help_text="Enlace de Google Maps de la clínica.",
                    ),
                ),

                (
                    "activo",
                    models.BooleanField(default=True),
                ),
            ],

            options={
                "verbose_name": "Configuración de Contacto",
                "verbose_name_plural": "Configuración de Contacto",
            },
        ),


        migrations.CreateModel(
            name="RedSocial",
            fields=[

                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),

                (
                    "nombre",
                    models.CharField(
                        help_text="Nombre que aparecerá en el enlace.",
                        max_length=50,
                    ),
                ),

                (
                    "url",
                    models.URLField(
                        help_text=(
                            "URL completa. Ejemplo: "
                            "https://www.facebook.com/..."
                        ),
                        max_length=500,
                    ),
                ),

                (
                    "icono",
                    models.CharField(
                        choices=[
                            ("facebook", "Facebook"),
                            ("instagram", "Instagram"),
                            ("tiktok", "TikTok"),
                            ("youtube", "YouTube"),
                            ("x", "X / Twitter"),
                            ("linkedin", "LinkedIn"),
                            ("whatsapp", "WhatsApp"),
                            ("telegram", "Telegram"),
                            ("globe", "Sitio web"),
                        ],
                        default="globe",
                        max_length=30,
                    ),
                ),

                (
                    "orden",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Menor número = aparece primero.",
                    ),
                ),

                (
                    "activo",
                    models.BooleanField(default=True),
                ),

                (
                    "nueva_pestana",
                    models.BooleanField(
                        default=True,
                        verbose_name="Abrir en nueva pestaña",
                    ),
                ),

            ],

            options={
                "verbose_name": "Red social",
                "verbose_name_plural": "Redes sociales",
                "ordering": ["orden", "id"],
            },
        ),
    ]