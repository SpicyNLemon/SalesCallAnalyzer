"""
Configuration and constants for the Sales Call Analyzer
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Model paths
MODEL_PATH = "./bert_emotion_model"

# Emotion configuration
EMOTION_LABELS = ["sadness", "joy", "love", "anger", "fear", "surprise"]
MAX_LENGTH = 128

# FFmpeg configuration
FFMPEG_BIN_PATH = os.path.join(os.getcwd(), "ffmpeg", "bin")

# Flags
BROWSER_OPENED_FLAG = os.path.join(os.getcwd(), 'browser_opened.flag')
