import os
from pydub import AudioSegment
import speech_recognition as sr
import tempfile

# Set FFmpeg path
ffmpeg_bin_dir = os.path.join(os.getcwd(), "ffmpeg", "bin")
os.environ["PATH"] = ffmpeg_bin_dir + ";" + os.environ.get("PATH", "")
AudioSegment.converter = "ffmpeg.exe"

test_file = "Audio files/The-Dragon-Prince-ALL-Rayllum-Moments-in-Season-5-sorvus-_720p_-h264_-youtube_.mp3"

print(f"Testing: {test_file}")
print(f"File exists: {os.path.exists(test_file)}")

try:
    # Load and convert
    audio = AudioSegment.from_file(test_file)
    print(f"Audio loaded: {len(audio)}ms duration")
    
    # Export to WAV
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        wav_path = tmp.name
    
    audio.export(wav_path, format="wav")
    print(f"Exported to WAV: {wav_path}")
    
    # Try speech recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        print(f"Audio recorded: {len(audio_data.frame_data)} bytes")
        
        try:
            text = recognizer.recognize_google(audio_data)
            print(f"SUCCESS! Transcribed: {text}")
        except sr.UnknownValueError:
            print("ERROR: Could not understand the audio (no speech detected)")
        except sr.RequestError as e:
            print(f"ERROR: Speech recognition failed: {e}")
    
    os.remove(wav_path)
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
