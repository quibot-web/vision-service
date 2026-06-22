from fastapi import FastAPI, Request
from pydantic import BaseModel
import base64
import openai
import os

app = FastAPI()

# Configura tu clave de API (ponla como variable de entorno en Coolify)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    base64_image = data.get("image_base64")
    
    # Llamada a GPT-4o para extraer datos (clonar la info)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analiza esta imagen de un producto. Extrae: nombre del producto, todo el texto legible, y una descripción del logo o marca en formato JSON."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                ],
            }
        ],
        response_format={ "type": "json_object" }
    )
    
    return response.choices[0].message.content