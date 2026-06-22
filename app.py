from fastapi import FastAPI, Request
import base64
import cv2
import numpy as np

app = FastAPI()

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    base64_str = data.get("image_base64")
    
    if not base64_str:
        return {"status": "error", "message": "No se recibió la imagen"}

    # Limpiar el string base64 si trae prefijo
    if "," in base64_str:
        base64_str = base64_str.split(",")[1]
    
    # Decodificar
    image_data = base64.b64decode(base64_str)
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return {"status": "error", "message": "OpenCV no pudo procesar el base64"}
        
    h, w = img.shape[:2]
    return {"status": "success", "width": w, "height": h}