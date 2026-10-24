# Examen-Arquitectura

Analizador de representación de datos hecho con Django. Permite convertir números entre bases binaria, octal, decimal y hexadecimal, y consultar la representación de caracteres.

## Requisitos

- Python 3.12 o posterior
- pip

## Ejecutar en Windows

Desde la carpeta del proyecto, crea y activa un entorno virtual e instala las dependencias:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Prepara la base de datos e inicia el servidor:

```powershell
python manage.py migrate
python manage.py runserver
```

Abre <http://127.0.0.1:8000/> en el navegador. Para detener el servidor, presiona `Ctrl+C` en PowerShell.

## Configuración

La base de datos SQLite, el entorno virtual y los archivos locales están excluidos de Git. Django usa una clave predeterminada solo para desarrollo; antes de desplegar el proyecto, define la variable de entorno `DJANGO_SECRET_KEY` con una clave secreta propia y configura `DEBUG` y `ALLOWED_HOSTS` para el entorno de producción.
