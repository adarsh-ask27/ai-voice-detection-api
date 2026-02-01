from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import io
import librosa
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

from audio_utils import preprocess_audio
from feature_extractor import extract_features
from model import predict

app = FastAPI(title="AI Voice Detection API")

class VoiceRequest(BaseModel):
    audio_url: str
    message: str | None = None

def load_audio_from_url(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "/"
    }

    r = requests.get(url, headers=headers, timeout=(5,10), stream=True)
    r.raise_for_status()

    audio_bytes = io.BytesIO(r.content)

    # 🔥 Load ONLY first 4 seconds (FAST)
    audio, sr = librosa.load(
        audio_bytes,
        sr=16000,
        mono=True,
        duration=4.0
    )

    return audio, sr
@app.get("/detect-voice")
def detect_voice_get():
    return {"message": "Use POST method for this endpoint"}
    
@app.post("/detect-voice")
def detect_voice(req: VoiceRequest):
    try:
        audio, sr = load_audio_from_url(req.audio_url)
        audio = preprocess_audio(audio, sr)

        features = extract_features(audio)
        classification, confidence, _ = predict(features)

        return {
            "prediction": classification,
            "confidence": round(float(confidence), 3)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
