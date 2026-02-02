import os

def predict_voice(audio_path: str):
    """
    Simple heuristic:
    - If audio size > threshold → Human
    - Else → AI
    """

    size_kb = os.path.getsize(audio_path) / 1024

    if size_kb > 40:
        return "Human", 0.85
    else:
        return "AI", 0.65
