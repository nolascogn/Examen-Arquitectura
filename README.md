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

## Publicar en Render

El archivo `render.yaml` configura un servicio web gratuito. Para desplegar:

1. Inicia sesión en [Render](https://render.com/) con GitHub y autoriza el acceso al repositorio `nolascogn/Examen-Arquitectura`.
2. En el panel de Render, elige **New** → **Blueprint** y selecciona ese repositorio.
3. Confirma la creación del servicio. Render generará una clave secreta y compilará la aplicación.
4. Cuando el despliegue termine, abre la URL `.onrender.com` que muestra Render y compártela.

El servicio gratuito puede tardar un poco en responder cuando vuelve a activarse tras un período sin uso. Esta aplicación no guarda datos de usuarios; la base SQLite del servicio no debe usarse para datos persistentes.
