FROM python:3.9-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar el archivo requirements.txt e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Comando para iniciar el servicio
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]