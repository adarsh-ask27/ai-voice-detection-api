API_KEY = "guvi-hcl-ai-voice-2026"
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
import base64
import tempfile
import os
from model import predict_voice

app = FastAPI(title="AI Voice Detection API")

# ✅ ACCEPT GUVI FIELD NAMES
class VoiceRequest(BaseModel):
    language: str
    audio_format: str = Field(alias="audioFormat")
    audio_base64: str = Field(alias="audioBase64")

    class Config:
        allow_population_by_field_name = True


@app.get("/")
def root():
    return {"status": "API running"}


@app.post("/detect-voice")
def detect_voice(data: VoiceRequest, x_api_key:str= Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    try:
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

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
