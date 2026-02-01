import librosa
import soundfile as sf
import os

input_dir = "data/human"
output_dir = "data/human_wav"

os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(input_dir):
    if file.endswith(".flac"):
        audio, sr = librosa.load(os.path.join(input_dir, file), sr=16000)
        out_path = os.path.join(output_dir, file.replace(".flac", ".wav"))
        sf.write(out_path, audio, sr)

print("Conversion done")