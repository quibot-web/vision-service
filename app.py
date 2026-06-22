from fastapi import FastAPI, Request, HTTPException
from openai import OpenAI # Importación moderna
import os

app = FastAPI()

# Inicializa el cliente moderno
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/analyze")
async def analyze(request: Request):
    try:
        data = await request.json()
        image_base64 = data.get("imagen_url")
        prompt = data.get("prompt_texto")

        if not image_base64:
            raise HTTPException(status_code=400, detail="No se recibió la imagen")

        if not image_base64.startswith("data:image/"):
            image_base64 = f"data:image/jpeg;base64,{image_base64}"

        # LLAMADA ACTUALIZADA A LA API
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