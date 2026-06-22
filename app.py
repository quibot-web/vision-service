from fastapi import FastAPI, Request, HTTPException
import openai
import os
import base64

app = FastAPI()

@app.post("/analyze")
async def analyze(request: Request):
    try:
        data = await request.json()
        api_key = data.get("openai_api_key")
        base64_image = data.get("image_base64")
        
        if not api_key:
            raise HTTPException(status_code=400, detail="Falta API Key")
        
        client = openai.OpenAI(api_key=api_key)
        
        # Llamada a GPT-4o
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analiza este producto. Devuelve un JSON con: nombre, texto_etiqueta, logo_descripcion, color_dominante."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                ],
            }],
            response_format={ "type": "json_object" }
        )
        
        return {"data": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))