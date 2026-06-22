from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # Leemos los datos binarios
    contents = await file.read()
    
    # Convertimos a un array de numpy
    nparr = np.frombuffer(contents, np.uint8)
    
    # Decodificamos la imagen
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        # Aquí sabremos si es un problema de formato de imagen
        return {
            "status": "error", 
            "message": "OpenCV no pudo decodificar la imagen",
            "received_size": len(contents),
            "content_type": file.content_type
        }
    
    h, w = img.shape[:2]
    return {"status": "success", "width": w, "height": h}