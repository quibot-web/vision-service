from fastapi import FastAPI, Request
import base64
import cv2
import numpy as np
# Necesitarías instalar: pip install easyocr
import easyocr 

app = FastAPI()
reader = easyocr.Reader(['es']) # Inicializamos el lector de texto en español

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    base64_str = data.get("image_base64").split(",")[1]
    image_data = base64.b64decode(base64_str)
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 1. DETECCIÓN DE TEXTO (Para logos y etiquetas)
    text_results = reader.readtext(img)
    textos_detectados = [res[1] for res in text_results]

    # 2. DETECCIÓN DE ESTRUCTURA (Aquí podrías integrar YOLO para objetos)
    # Por ahora, extraemos los datos básicos de la imagen
    h, w, _ = img.shape
    
    return {
        "status": "success",
        "dimensiones": {"w": w, "h": h},
        "textos": textos_detectados,
        "analisis_logico": "Imagen escaneada para extraer etiquetas y textos"
    }