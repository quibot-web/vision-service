from fastapi import FastAPI, UploadFile
import cv2
import numpy as np

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile):
    # Leer la imagen desde n8n
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Análisis técnico: dimensiones
    h, w = img.shape[:2]
    
    # Análisis de bordes (Canny) para detectar la forma del producto
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    
    # Obtener el recuadro que encierra al producto (Bounding Box)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w_obj, h_obj = cv2.boundingRect(max(contours, key=cv2.contourArea))
    else:
        x, y, w_obj, h_obj = 0, 0, w, h
        
    return {
        "ancho_total": w, "alto_total": h,
        "producto_pos": {"x": x, "y": y, "w": w_obj, "h": h_obj},
        "status": "success"
    }