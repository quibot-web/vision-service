from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np

app = FastAPI()

# Aceptamos cualquier nombre de archivo (Field alias)
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # Leemos los bytes del archivo
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return {"status": "error", "message": "No se pudo decodificar la imagen"}
    
    h, w = img.shape[:2]
    return {"status": "success", "width": w, "height": h}