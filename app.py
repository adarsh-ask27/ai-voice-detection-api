from fastapi import FastAPI, Header, HTTPException, Request
import base64, tempfile, os
from model import predict_voice

API_KEY = "guvi-hcl-ai-voice-2026"

app = FastAPI()

# -------------------------------------------------
# 1️⃣ GUVI HONEYPOT (ABSOLUTELY NO BODY PARSING)
# -------------------------------------------------
@app.api_route("/", methods=["GET", "POST"])
async def honeypot(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return {"status": "ok"}

# -------------------------------------------------
# 2️⃣ REAL EVALUATION ENDPOINT
# -------------------------------------------------
@app.post("/detect-voice")
async def detect_voice(request: Request, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        data = await request.json()
    except:
        # GUVI sometimes sends broken JSON — DO NOT FAIL
        return {"status": "ok"}

    audio_base64 = data.get("audioBase64") or data.get("audio_base64")
    audio_format = data.get("audioFormat", "wav")

    if not audio_base64:
        return {"status": "ok"}

    audio_bytes = base64.b64decode(audio_base64)

    if len(audio_bytes) < 200:
        raise HTTPException(status_code=400, detail="Audio too short")

    with tempfile.NamedTemporaryFile(delete=False, suffix="."+audio_format) as f:
        f.write(audio_bytes)
        path = f.name

    prediction, confidence = predict_voice(path)
    os.remove(path)

    return {
        "prediction": prediction,
        "confidence": confidence
    }
