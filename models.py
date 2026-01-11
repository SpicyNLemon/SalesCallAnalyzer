"""
Model loading and emotion prediction logic
"""
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from config import MODEL_PATH, EMOTION_LABELS, MAX_LENGTH


class EmotionPredictor:
    """Handles BERT model loading and emotion predictions"""
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
        self.model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
        self.model.to(self.device)
        self.model.eval()
    
    def predict(self, text):
        """
        Predict emotion from text
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            tuple: (predicted_emotion, probabilities)
        """
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            padding=True, 
            truncation=True, 
            max_length=MAX_LENGTH
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)
            pred = torch.argmax(probs, dim=1).item()
        
        return EMOTION_LABELS[pred], probs.cpu().numpy()[0]
    
    def predict_with_percentages(self, text):
        """
        Predict emotion and return probabilities as percentages
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Dictionary with prediction, top_3, and other_emotions
        """
        emotion, probabilities = self.predict(text)
        
        # Convert to percentages and get top 3
        prob_dict = dict(zip(EMOTION_LABELS, probabilities))
        sorted_probs = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)
        
        top_3 = {e: float(p * 100) for e, p in sorted_probs[:3]}
        other_emotions = {e: float(p * 100) for e, p in sorted_probs[3:]}
        
        return {
            "prediction": emotion,
            "top_3": top_3,
            "other_emotions": other_emotions
        }
