from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse # Importante
import cv2
import numpy as np

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return JSONResponse(status_code=400, content={"status": "error", "message": "No se pudo leer la imagen"})
    
    h, w = img.shape[:2]
    # Retornamos un JSON response explícito
    return JSONResponse(content={"status": "success", "width": w, "height": h})