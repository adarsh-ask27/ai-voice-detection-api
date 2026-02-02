from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
import tempfile
import os

from model import predict_voice

app = FastAPI(title="AI Voice Detection API")

# -------- Request Schema (GUVI FORMAT) --------
class VoiceRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: str


@app.get("/")
def root():
    return {"status": "API running"}


@app.post("/detect-voice")
def detect_voice(data: VoiceRequest):
    try:
        # Decode Base64
        audio_bytes = base64.b64decode(data.audio_base64)

        # Reject very small audio
        if len(audio_bytes) < 15000:
            raise HTTPException(status_code=400, detail="Audio too short")

        # Save temp audio file
        suffix = "." + data.audio_format.lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            f.write(audio_bytes)
            temp_audio_path = f.name

        # Predict
        prediction, confidence = predict_voice(temp_audio_path)

        # Cleanup
        os.remove(temp_audio_path)

        return {
            "prediction": prediction,
            "confidence": confidence
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
