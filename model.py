import joblib
import numpy as np

MODEL_PATH = "models/voice_detector.pkl"
model = joblib.load(MODEL_PATH)

def predict(features):
    
    proba = model.predict_proba([features])[0]

    # Handle single-class model safely
    if len(proba) == 1:
        prob_ai = 0.0
    else:
        prob_ai = proba[1]  # AI probability
    classification = "AI_generated" if prob_ai > 0.5 else "Human"

    explanation = {
        "spectral_smoothness": round(float(features[-1]), 3),
        "pitch_variance": round(float(features[-2]), 3),
    }

    return classification, float(prob_ai), {}