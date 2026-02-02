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

@app.post("/detect-voice")
async def honeypot_guard(
    request: Request,
    x_api_key: str = Header(None)
):
    # Honeypot check (NO BODY EXPECTED)
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # If body is empty → honeypot test
    body = await request.body()
    if not body:
        return {
            "status": "alive",
            "message": "Honeypot check passed"
        }

    # If body exists → forward to real logic
    data = VoiceRequest.parse_raw(body)

    audio_bytes = base64.b64decode(data.audio_base64)

    if len(audio_bytes) < 200:
        raise HTTPException(status_code=400, detail="Audio too short")

    suffix = "." + data.audio_format.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
        f.write(audio_bytes)
        temp_path = f.name

    prediction, confidence = predict_voice(temp_path)
    os.remove(temp_path)

    return {
        "prediction": prediction,
        "confidence": confidence
    }
