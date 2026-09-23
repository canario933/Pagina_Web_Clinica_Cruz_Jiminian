# Clínica Cruz Jiminian

Sistema web para la gestión y presentación digital de la Clínica Cruz Jiminian.

El proyecto está desarrollado con Django y permite administrar médicos, especialidades, servicios, horarios médicos, citas y contenido institucional desde el panel de administración.

---

## 📋 Requisitos

Antes de ejecutar el proyecto es necesario tener instalado:

- Python 3.x
- Git
- pip

Se recomienda utilizar Windows PowerShell para seguir estas instrucciones.

---

## 📥 1. Clonar el proyecto

Abrir PowerShell y ejecutar:

```powershell
git clone https://github.com/canario933/Pagina_Web_Clinica_Cruz_Jiminian.git

---
## 📥 2. Crear el entorno virtual

```powershell
python -m venv .venv

---

## 3. Instalar las dependencias

```powershell
pip install -r requirements.txt

---

## 4. Crear la base de datos

```powershell
python manage.py migrate

---
## 5. Crear el usuario administrador

```powershell
python manage.py createsuperuser

---
## 6. Carpeta Media

```powershell
mkdir Media

---
## 7. Ejecutar el proyecto

```powershell
python manage.py runserver
