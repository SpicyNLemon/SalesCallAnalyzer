import os
from pydub import AudioSegment

# Set ffmpeg path for pydub (local installation)
ffmpeg_bin_dir = os.path.join(os.getcwd(), "ffmpeg", "bin")
os.environ["PATH"] = ffmpeg_bin_dir + ";" + os.environ.get("PATH", "")
AudioSegment.converter = "ffmpeg.exe"
AudioSegment.ffprobe = "ffprobe.exe"

print("Current dir:", os.getcwd())
print("FFmpeg bin dir added to PATH")
print("Converter set to:", AudioSegment.converter)

# Try to load a test audio file if it exists
test_file = "temp_audio.wav"
if os.path.exists(test_file):
    try:
        audio = AudioSegment.from_file(test_file)
        print("Audio loaded successfully")
    except Exception as e:
        print("Error loading audio:", e)
else:
    print("No test audio file found")