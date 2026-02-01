import joblib
import os

MODEL_PATH = "models/voice_detector.pkl"
_model = None

def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("Model file not found")
        _model = joblib.load(MODEL_PATH)
    return _model

def predict(features):
    model = get_model()
    prob = model.predict_proba([features])[0][1]

    classification = "AI_GENERATED" if prob > 0.5 else "HUMAN"

    explanation = {
        "spectral_smoothness": round(float(features[-1]), 3),
        "pitch_variance": round(float(features[-2]), 3)
    }

    return classification, float(prob), explanation
