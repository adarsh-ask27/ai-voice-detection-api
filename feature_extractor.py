import numpy as np
import librosa

def extract_features(audio, sr=16000):
    features = []

    # MFCCs
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=20)
    features.extend(np.mean(mfccs, axis=1))
    features.extend(np.std(mfccs, axis=1))

    # Spectral features
    spec_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)
    features.append(np.mean(spec_centroid))
    features.append(np.std(spec_centroid))

    spec_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)
    features.append(np.mean(spec_rolloff))

    # Zero Crossing Rate
    zcr = librosa.feature.zero_crossing_rate(audio)
    features.append(np.mean(zcr))


    # Prosody smoothness (AI voices are too smooth)
    features.append(np.std(audio))

    return np.array(features)