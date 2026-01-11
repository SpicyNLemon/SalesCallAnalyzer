# AI Sales Call Analyzer

A Flask web app that analyzes emotions in text and audio using a fine-tuned BERT model. Upload text or audio files to get emotion predictions.

## Features
- **Text Analysis**: Input text and get emotion predictions (e.g., joy, sadness, anger).
- **Audio Analysis**: Upload audio files (WAV, MP3, etc.) for transcription and emotion analysis.
- **Modern UI**: Bootstrap-based interface with custom styling.

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- FFmpeg (for audio processing)

### 2. Install FFmpeg (Required for Audio)
FFmpeg is needed to process audio files.

- Download from: https://ffmpeg.org/download.html
- Choose "Windows builds" from gyan.dev.
- Extract the ZIP to a folder (e.g., `C:\Users\ASUS\Downloads\ffmpeg-8.0.1` or your preferred location).
- **Add FFmpeg to PATH** (so Windows can find it):
  1. Press **Win + R**, type `sysdm.cpl`, and press Enter (opens System Properties).
  2. Click **Advanced** > **Environment Variables**.
  3. Under **System variables**, find **Path**, select it, and click **Edit**.
  4. Click **New** and paste the path to the `bin` folder (e.g., `C:\Users\ASUS\Downloads\ffmpeg-8.0.1\bin`).
  5. Click **OK** on all windows to save.
- Restart your terminal/VS Code and verify: Run `ffmpeg -version` in the terminal. It should show version info if successful.

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
python app.py
```
- The app will auto-open in your browser at `http://127.0.0.1:5000`.
- If not, open the URL manually.

### 5. Usage
- **Text**: Enter text in the input field and submit.
- **Audio**: Choose an audio file, upload, and wait for transcription/emotion results.
- Supported formats: WAV, MP3, FLAC, OGG, etc.

## Project Structure
- `app.py`: Main Flask application.
- `templates/index.html`: Web UI.
- `static/style.css`: Custom styles.
- `bert_emotion_model/`: Pre-trained BERT model files.
- `requirements.txt`: Python dependencies.

## Notes
- Audio transcription uses Google's API (requires internet).
- The BERT model is trained on general emotion data; for sales-specific accuracy, fine-tune on more data.
- For issues, check the console for errors.

## License
[Add your license here]