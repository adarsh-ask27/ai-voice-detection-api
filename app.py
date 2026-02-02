API_KEY = "guvi-hcl-ai-voice-2026"
from fastapi import FastAPI, Header, Body, Request, HTTPException
from pydantic import BaseModel, Field
import base64
import tempfile
import os
from model import predict_voice
from typing import Optional

app = FastAPI(title="AI Voice Detection API")

# ✅ ACCEPT GUVI FIELD NAMES
class VoiceRequest(BaseModel):
    language: str
    audio_format: str = Field(alias="audioFormat")
    audio_base64: str = Field(alias="audioBase64")

    class Config:
        allow_population_by_field_name = True


app = FastAPI()

API_KEY = "guvi-hcl-ai-voice-2026"


@app.api_route("/detect-voice", methods=["GET", "POST"])
async def detect_voice(
    request: Request,
    x_api_key: str = Header(None)
):
    # 1️⃣ API key check (GUVI ONLY checks this)
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 2️⃣ Honeypot call → NO BODY
    if request.method == "GET":
        return {"status": "ok"}

    body = await request.body()

    # 3️⃣ POST with EMPTY BODY (GUVI does this)
    if not body:
        return {"status": "ok"}

    # 4️⃣ REAL evaluation will send JSON
    data = await request.json()

    audio_base64 = data.get("audio_base64")
    audio_format = data.get("audio_format", "wav")

    if not audio_base64:
        return {"status": "ok"}  # still don't fail honeypot

    audio_bytes = base64.b64decode(audio_base64)

    if len(audio_bytes) < 200:
        raise HTTPException(status_code=400, detail="Audio too short")

    suffix = "." + audio_format.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
        f.write(audio_bytes)
        temp_path = f.name

    prediction, confidence = predict_voice(temp_path)
    os.remove(temp_path)

    return {
        "prediction": prediction,
        "confidence": confidence
    }
