from fastapi import FastAPI, Request, HTTPException
import openai
import os

app = FastAPI()

# Configura tu clave de API (asegúrate de tenerla en las variables de entorno de Coolify)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/analyze")
async def analyze(request: Request):
    try:
        data = await request.json()
        image_base64 = data.get("imagen_url")
        prompt = data.get("prompt_texto")

        if not image_base64:
            raise HTTPException(status_code=400, detail="No se recibió la imagen")

        # Añadir prefijo para que OpenAI reconozca el formato
        if not image_base64.startswith("data:image/"):
            image_base64 = f"data:image/jpeg;base64,{image_base64}"

        # Llamada a la API de OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o", # O el modelo que estés usando
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