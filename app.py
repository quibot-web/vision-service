from fastapi import FastAPI, Request, HTTPException
from openai import OpenAI

app = FastAPI()

@app.post("/analyze")
async def analyze(request: Request):
    try:
        data = await request.json()
        user_openai_key = data.get("openai_api_key")
        image_base64 = data.get("imagen_url")

        if not user_openai_key or not image_base64:
            raise HTTPException(status_code=400, detail="Faltan datos (API Key o Imagen)")

        client = OpenAI(api_key=user_openai_key)

        # Formatear la imagen
        if not image_base64.startswith("data:image/"):
            image_base64 = f"data:image/jpeg;base64,{image_base64}"

        # LLAMADA DIRECTA: Pedimos descripción detallada sin sesgos
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": "Analiza esta imagen con máximo detalle. Describe los objetos, colores, texturas, iluminación, composición y cualquier elemento visible. Sé técnico y descriptivo."
                        },
                        {"type": "image_url", "image_url": {"url": image_base64}},
                    ],
                }
            ],
            max_tokens=500,
        )

        return {"analisis": response.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))