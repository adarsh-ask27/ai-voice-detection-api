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


@app.get("/detect-voice")
def honeypot_check(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return {
        "status": "alive",
        "message": "Honeypot check passed"
    }

API_KEY = "guvi-hcl-ai-voice-2026"

@app.post("/detect-voice")
async def detect_voice(
    request: Request,
    x_api_key: Optional[str] = Header(None)
):
    # 1️⃣ API key check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 2️⃣ Read body safely
    try:
        body = await request.json()
    except:
        body = {}

    # 🔑 HONEYPOT MODE (NO AUDIO SENT)
    if "audio_base64" not in body:
        return {
            "status": "ok",
            "message": "Honeypot authentication successful"
        }

    # 3️⃣ REAL VOICE DETECTION MODE
    audio_base64 = body["audio_base64"]
    audio_format = body.get("audio_format", "wav")

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
