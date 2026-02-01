import base64
import io
import librosa
import numpy as np
import soundfile as sf

TARGET_SR = 16000
MIN_DURATION = 2.0  # seconds

def decode_audio(base64_audio: str):
    audio_bytes = base64.b64decode(base64_audio)
    audio_buffer = io.BytesIO(audio_bytes)
    audio, sr = sf.read(audio_buffer)
    return audio, sr

def preprocess_audio(audio, sr):
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)  # mono

    audio = librosa.resample(audio, orig_sr=sr, target_sr=TARGET_SR)
    # audio, _ = librosa.effects.trim(audio)

    duration = len(audio) / TARGET_SR
    if duration < MIN_DURATION:
        raise ValueError("Audio too short")

    audio = librosa.util.normalize(audio)
    return audio