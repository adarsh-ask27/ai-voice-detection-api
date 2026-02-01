from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from audio_utils import decode_audio, preprocess_audio
from feature_extractor import extract_features
from model import predict

app = FastAPI(title="AI Voice Detection API")


class VoiceRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64_format: str


@app.get("/detect-voice")
def detect_voice_get():
    return {"message": "Use POST method for this endpoint"}


@app.post("/detect-voice")
def detect_voice(req: VoiceRequest):
    try:
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
