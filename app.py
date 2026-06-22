from fastapi import FastAPI, Request, HTTPException
from openai import OpenAI
import os

app = FastAPI()

@app.post("/analyze")
async def analyze(request: Request):
    try:
        data = await request.json()
        
        # Obtenemos la clave directamente desde el JSON que llega de n8n
        user_openai_key = data.get("openai_api_key")
        image_base64 = data.get("imagen_url")
        prompt = data.get("prompt_texto")

        if not user_openai_key:
            raise HTTPException(status_code=400, detail="Falta la API Key en la petición")

        # Inicializamos el cliente con la clave del usuario
        client = OpenAI(api_key=user_openai_key)

        # Formatear la imagen para OpenAI
        if not image_base64.startswith("data:image/"):
            image_base64 = f"data:image/jpeg;base64,{image_base64}"

        # Llamada a OpenAI
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_base64}},
                    ],
                }
            ],
            max_tokens=300,
        )

        return {"resultado": response.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))