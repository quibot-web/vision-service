from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
import logging

# Configurar logs para ver qué pasa en Coolify
logging.basicConfig(level=logging.INFO)
app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        logging.info(f"Recibido archivo: {file.filename}")
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return {"status": "error", "message": "OpenCV no pudo decodificar el buffer"}
            
        h, w = img.shape[:2]
        return {"status": "success", "width": w, "height": h}
    except Exception as e:
        logging.error(f"Error procesando: {str(e)}")
        return {"status": "error", "message": str(e)}