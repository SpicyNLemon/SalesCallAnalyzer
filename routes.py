"""
Flask routes for the Sales Call Analyzer
"""
from flask import render_template, request, send_from_directory, make_response, Blueprint
from models import EmotionPredictor
from audio_processor import AudioProcessor
import os
import logging

logger = logging.getLogger(__name__)

routes = Blueprint('routes', __name__)


@routes.route('/favicon.ico')
def favicon():
    """Serve favicon with no-cache headers"""
    response = make_response(
        send_from_directory(
            os.path.join(routes.root_path, 'static'), 
            'Icon.png', 
            mimetype='image/png'
        )
    )
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@routes.route("/", methods=["GET", "POST"])
def index():
    """Home page route for text-based emotion analysis"""
    prediction = None
    probabilities = None
    
    if request.method == "POST":
        text = request.form.get("text_input", "").strip()
        if text:
            predictor = EmotionPredictor()
            prediction, probs = predictor.predict(text)
            probabilities = dict(zip(
                ["sadness", "joy", "love", "anger", "fear", "surprise"],
                [float(p) for p in probs]
            ))
    
    return render_template(
        "index.html", 
        prediction=prediction, 
        probabilities=probabilities
    )


@routes.route("/upload_audio", methods=["POST"])
def upload_audio():
    """Audio upload and emotion analysis endpoint"""
    if 'file' not in request.files:
        return {"error": "No file part"}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {"error": "No selected file"}, 400
    
    # Process audio file
    text, success, error = AudioProcessor.process_audio_file(file)
    
    if not success:
        logger.error(f"Audio processing failed: {error}")
        return {"error": error}, 500
    
    # Predict emotion
    predictor = EmotionPredictor()
    result = predictor.predict_with_percentages(text)
    result["transcript"] = text
    
    return result
