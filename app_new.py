"""
Sales Call Analyzer - Main Application Entry Point
"""
from flask import Flask
import os
import threading
import time
import webbrowser
from pydub import AudioSegment
from config import FFMPEG_BIN_PATH, BROWSER_OPENED_FLAG
from routes import routes
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure ffmpeg path for pydub
if os.path.exists(FFMPEG_BIN_PATH):
    os.environ['PATH'] = FFMPEG_BIN_PATH + os.pathsep + os.environ.get('PATH', '')
    logger.info("FFmpeg path configured")

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(routes)


def open_browser():
    """Open browser after server starts"""
    time.sleep(1)
    if not os.path.exists(BROWSER_OPENED_FLAG):
        webbrowser.open("http://127.0.0.1:5000/")
        # Create flag file to prevent multiple opens
        with open(BROWSER_OPENED_FLAG, 'w') as f:
            f.write('')


if __name__ == "__main__":
    logger.info("Starting Sales Call Analyzer...")
    
    # Start browser in separate thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Run Flask app
    app.run(debug=False)
