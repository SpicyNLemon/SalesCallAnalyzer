"""
Audio processing utilities for transcription and conversion
"""
import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
import traceback
import logging

logger = logging.getLogger(__name__)


class AudioProcessor:
    """Handles audio file processing and transcription"""
    
    @staticmethod
    def convert_to_wav(input_path):
        """
        Convert audio file to WAV format
        
        Args:
            input_path (str): Path to input audio file
            
        Returns:
            str: Path to converted WAV file
        """
        logger.info(f"Loading audio from: {input_path}")
        audio = AudioSegment.from_file(input_path)
        logger.info("Audio loaded successfully, converting to WAV...")
        
        wav_path = input_path + ".wav"
        audio.export(wav_path, format="wav")
        logger.info(f"WAV exported to: {wav_path}")
        
        return wav_path
    
    @staticmethod
    def transcribe_audio(wav_path):
        """
        Transcribe audio file using Google Speech Recognition
        
        Args:
            wav_path (str): Path to WAV file
            
        Returns:
            str: Transcribed text
        """
        logger.info("Starting transcription...")
        recognizer = sr.Recognizer()
        
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        
        logger.info(f"Transcription complete: {text[:100]}...")
        return text
    
    @staticmethod
    def cleanup_temp_files(temp_path, wav_path=None):
        """
        Clean up temporary files
        
        Args:
            temp_path (str): Path to original temp file
            wav_path (str, optional): Path to WAV file if different
        """
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
                logger.debug(f"Removed temp file: {temp_path}")
            
            if wav_path and os.path.exists(wav_path):
                os.remove(wav_path)
                logger.debug(f"Removed WAV file: {wav_path}")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
    
    @staticmethod
    def process_audio_file(file):
        """
        Process uploaded audio file and return transcription
        
        Args:
            file: Flask FileStorage object
            
        Returns:
            tuple: (text, success, error_message)
        """
        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            file.save(temp_path)
        
        wav_path = None
        try:
            wav_path = AudioProcessor.convert_to_wav(temp_path)
            text = AudioProcessor.transcribe_audio(wav_path)
            return text, True, None
        
        except Exception as e:
            logger.error(f"Error processing audio: {str(e)}")
            traceback.print_exc()
            return None, False, str(e)
        
        finally:
            AudioProcessor.cleanup_temp_files(temp_path, wav_path)
