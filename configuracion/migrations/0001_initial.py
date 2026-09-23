# Generated manually for the hero background configuration.
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ConfiguracionHero",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fondo", models.FileField(help_text="Imagen, GIF o video. Formatos: JPG, JPEG, PNG, WEBP, GIF, MP4 o WEBM.", upload_to="hero/")),
                ("titulo", models.CharField(default="Cuidamos tu salud, cuidamos de ti.", max_length=120)),
                ("subtitulo", models.TextField(blank=True, default="Atención médica profesional, humana y cercana, porque tu bienestar y el de tu familia merecen lo mejor.")),
                ("overlay", models.PositiveSmallIntegerField(default=75, help_text="Oscurecimiento del fondo para mejorar la lectura del texto (0 a 100%).")),
                ("activo", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Configuración del Hero",
                "verbose_name_plural": "Configuración del Hero",
            },
        ),
    ]
