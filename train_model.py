import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from feature_extractor import extract_features
import librosa

X = []
y = []

DATASET = {
    "human": "data/human/",
    "ai": "data/ai/"
}

for label, folder in DATASET.items():
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        audio, sr = librosa.load(path, sr=16000)
        features = extract_features(audio)
        X.append(features)
        y.append(0 if label == "human" else 1)

X = np.array(X)
y = np.array(y)

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    min_samples_split=4,
    class_weight="balanced",
    random_state=42
)
print("Class distribution:",np.bincount(y))
model.fit(X, y)

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/voice_detector.pkl")

print("✅ Model trained and saved")