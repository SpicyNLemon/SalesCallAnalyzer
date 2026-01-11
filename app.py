from flask import Flask, render_template, request, send_from_directory, make_response
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import numpy as np
import threading
import time
import webbrowser
import os
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
from datetime import datetime

# Configure ffmpeg path for pydub
ffmpeg_bin_path = os.path.join(os.getcwd(), "ffmpeg", "bin")
if os.path.exists(ffmpeg_bin_path):
    # Add to PATH so pydub can find ffmpeg and ffprobe
    os.environ['PATH'] = ffmpeg_bin_path + os.pathsep + os.environ.get('PATH', '')

# Initialize Flask app
app = Flask(__name__)

# Flag to prevent multiple browser opens
browser_opened_flag = os.path.join(os.getcwd(), 'browser_opened.flag')

# Load the trained model and tokenizer
model_path = "./bert_emotion_model"  # Relative path to your model
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

# Emotion labels
emotion_labels = ["sadness", "joy", "love", "anger", "fear", "surprise"]
max_length = 128

# Prediction function
def predict_emotion(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)
        pred = torch.argmax(probs, dim=1).item()
    return emotion_labels[pred], probs.cpu().numpy()[0]

# Routes
@app.route('/favicon.ico')
def favicon():
    response = make_response(send_from_directory(os.path.join(app.root_path, 'static'), 'Icon.png', mimetype='image/png'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    probabilities = None
    if request.method == "POST":
        text = request.form["text_input"]
        prediction, probabilities = predict_emotion(text)
        probabilities = dict(zip(emotion_labels, [float(p) for p in probabilities]))
    return render_template("index.html", prediction=prediction, probabilities=probabilities)

@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    if 'file' not in request.files:
        return {"error": "No file part"}, 400
    file = request.files['file']
    if file.filename == '':
        return {"error": "No selected file"}, 400
    
    # Save uploaded file with original extension
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_path = temp_file.name
        file.save(temp_path)
    
    wav_path = None
    try:
        # Convert to wav using pydub
        print(f"Loading audio from: {temp_path}")
        audio = AudioSegment.from_file(temp_path)
        print(f"Audio loaded successfully, converting to WAV...")
        
        # Export as WAV
        wav_path = temp_path + ".wav"
        audio.export(wav_path, format="wav")
        print(f"WAV exported to: {wav_path}")
        
        # Transcribe
        print(f"Starting transcription...")
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        
        print(f"Transcription: {text}")
        
        # Predict emotion
        prediction, probabilities = predict_emotion(text)
        
        # Convert to percentages and get top 3
        prob_dict = dict(zip(emotion_labels, probabilities))
        sorted_probs = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)
        
        top_3 = {emotion: float(prob * 100) for emotion, prob in sorted_probs[:3]}
        other_emotions = {emotion: float(prob * 100) for emotion, prob in sorted_probs[3:]}
        
        return {
            "prediction": prediction, 
            "top_3": top_3,
            "other_emotions": other_emotions,
            "transcript": text
        }
    except Exception as e:
        print(f"Error in upload_audio: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}, 500
    finally:
        # Clean up
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if wav_path and os.path.exists(wav_path):
                os.remove(wav_path)
        except Exception as cleanup_err:
            print(f"Cleanup error: {cleanup_err}")

if __name__ == "__main__":
    def open_browser():
        time.sleep(1)
        webbrowser.open("http://127.0.0.1:5000/")
    
    threading.Thread(target=open_browser).start()
    app.run()