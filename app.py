from fastapi import FastAPI, Request, HTTPException
from openai import OpenAI
from supabase import create_client, Client
import os

app = FastAPI()

# Inicializamos SOLO Supabase, porque las credenciales de DB sí son fijas en Coolify
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.post("/analyze")
async def analyze(request: Request):
    try:
        data = await request.json()
        user_id = data.get("user_id") 
        image_base64 = data.get("imagen_url")
        prompt = data.get("prompt_texto")

        # 1. Consultar Supabase dinámicamente
        response_db = supabase.table("usuarios").select("openai_key").eq("id", user_id).single().execute()
        user_openai_key = response_db.data.get("openai_key")

        if not user_openai_key:
            raise HTTPException(status_code=401, detail="No se encontró API Key para este usuario")

        # 2. Inicializar cliente de OpenAI AQUÍ, con la clave obtenida
        client = OpenAI(api_key=user_openai_key)

        # 3. Resto de la lógica...
        if not image_base64.startswith("data:image/"):
            image_base64 = f"data:image/jpeg;base64,{image_base64}"

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": image_base64}}]}]
        )

        return {"resultado": response.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))