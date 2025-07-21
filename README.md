# Birthday Invitation Web App

Este proyecto es una aplicación web para gestionar invitaciones de cumpleaños. Está desarrollado con FastAPI y diseñado para ser desplegado en Render.com.

## Características
- Confirmación de asistencia a la cena.
- Compra de entradas para la fiesta posterior.
- Panel de administración para gestionar las confirmaciones.

## Tecnologías utilizadas
- **Backend**: FastAPI
- **Frontend**: Jinja2, Tailwind CSS, Alpine.js
- **Base de datos**: SQLite

## Instrucciones de despliegue
1. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecutar la aplicación localmente:
   ```bash
   uvicorn main:app --reload
   ```
3. Desplegar en Render.com utilizando el archivo `render.yaml`.
