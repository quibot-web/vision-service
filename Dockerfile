FROM python:3.9-slim

# Instalar dependencias del sistema necesarias para OpenCV
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

# Instalar librerías de Python
RUN pip install fastapi uvicorn opencv-python-headless python-multipart

# Copiar el código de la aplicación
COPY . .

# Comando para iniciar el servicio
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]