FROM python:3.9-slim
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN pip install fastapi uvicorn opencv-python-headless python-multipart
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]