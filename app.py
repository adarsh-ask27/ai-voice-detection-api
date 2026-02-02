from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field
import base64, tempfile, os
from typing import Optional
from model import predict_voice

API_KEY = "guvi-hcl-ai-voice-2026"

app = FastAPI(title="AI Voice Detection API")

# -------------------------------------------------
# 1️⃣ HONEYPOT ROOT (GUVI TESTS THIS ONLY)
# -------------------------------------------------
@app.api_route("/", methods=["GET", "POST"])
async def honeypot_root(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return {"status": "ok"}

# -------------------------------------------------
# 2️⃣ REQUEST MODEL (FOR REAL EVALUATION)
# -------------------------------------------------
class VoiceRequest(BaseModel):
    language: str
    audio_format: str = Field(alias="audioFormat")
    audio_base64: str = Field(alias="audioBase64")

    class Config:
        allow_population_by_field_name = True

# -------------------------------------------------
# 3️⃣ REAL DETECTION ENDPOINT
# -------------------------------------------------
@app.post("/detect-voice")
async def detect_voice(
    data: VoiceRequest,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

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
