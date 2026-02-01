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
from pydantic import BaseModel

app = FastAPI(title="AI Voice Detection API")

class VoiceRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64_format: str

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
    audio, sr = decode_audio(req.audio_base64_format)
    audio = preprocess_audio(audio, sr)
    features = extract_features(audio)

    classification, confidence, explanation = predict(features)

    return {
        "classification": classification,
        "confidence": round(confidence, 3),
        "language": req.language,
        "explanation": explanation
    }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
