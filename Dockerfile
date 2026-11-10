# Imagen base: Python 3.12 en versión liviana
FROM python:3.12-slim

# No generar archivos .pyc y mostrar los logs al instante
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Primero solo requirements, así Docker reutiliza la instalación si no cambió
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Después el resto del código (lo que no esté en .dockerignore)
COPY . .

# Juntar los archivos estáticos durante el build
# (SECRET_KEY falsa solo para este paso; la real se pasa al ejecutar)
RUN SECRET_KEY=solo-para-build python manage.py collectstatic --noinput

EXPOSE 8000

# Al arrancar: aplicar migraciones y levantar Daphne (servidor ASGI)
CMD ["sh", "-c", "python manage.py migrate --noinput && daphne -b 0.0.0.0 -p ${PORT:-8000} config.asgi:application"]