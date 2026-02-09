import os
import json
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import librosa
import numpy as np
from transformers import pipeline
import speech_recognition as sr
import subprocess
import imageio_ffmpeg
from datetime import timedelta
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Initialize sentiment analysis pipeline
try:
    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=-1  # CPU
    )
except Exception as e:
    print(f"Error loading sentiment model: {e}")
    sentiment_analyzer = None


def convert_to_wav(audio_path):
    """Convert audio file to WAV format using ffmpeg directly"""
    try:
        # If file is already wav, we might still want to convert to ensure correct encoding (PCM)
        # But for now let's assume if it ends in .wav it's fine, unless we want to force re-encoding.
        # Let's force re-encoding to 'wav_path' to ensure it's 16kHz PCM which helps speech recognition.
        
        base_path = audio_path.rsplit('.', 1)[0]
        wav_path = f"{base_path}_converted.wav"
        
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        
        # Command: ffmpeg -i input -ar 16000 -ac 1 -y output.wav
        # -ar 16000: Resample to 16kHz (good for SR)
        # -ac 1: Mono (good for SR)
        # -y: Overwrite
        command = [
            ffmpeg_exe, 
            '-i', audio_path,
            '-ar', '16000',
            '-ac', '1',
            '-y', 
            wav_path
        ]
        
        # Capture output for debugging
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return wav_path
        
    except subprocess.CalledProcessError as e:
        error_msg = f"FFmpeg conversion failed: {e.stderr}"
        print(error_msg)
        raise Exception(error_msg)
    except Exception as e:
        print(f"Error converting audio: {e}")
        raise

def analyze_audio_sentiment(audio_path):
    """Analyze sentiment from audio file with timestamps"""
    try:
        # Convert to WAV if needed
        wav_path = convert_to_wav(audio_path)
        
        # Load audio file
        audio, sr_rate = librosa.load(wav_path, sr=16000)
        duration = librosa.get_duration(y=audio, sr=sr_rate)
        
        # Initialize speech recognizer
        recognizer = sr.Recognizer()
        
        # Process audio in chunks (every 3 seconds)
        chunk_duration = 3.0  # seconds
        results = []
        
        with sr.AudioFile(wav_path) as source:
            for start_time in np.arange(0, duration, chunk_duration):
                end_time = min(start_time + chunk_duration, duration)
                
                # Read audio chunk
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                try:
                    audio_chunk = recognizer.record(source, duration=chunk_duration)
                    
                    # Transcribe audio chunk
                    text = recognizer.recognize_google(audio_chunk)
                    
                    if text and sentiment_analyzer:
                        # Analyze sentiment
                        sentiment = sentiment_analyzer(text[:512])[0]  # Limit text length
                        
                        # Map sentiment to emotion categories
                        label = sentiment['label']
                        score = sentiment['score']
                        
                        # Enhanced emotion mapping
                        if label == 'POSITIVE':
                            if score > 0.9:
                                emotion = 'Very Happy'
                            elif score > 0.7:
                                emotion = 'Happy'
                            else:
                                emotion = 'Positive'
                        else:  # NEGATIVE
                            if score > 0.9:
                                emotion = 'Very Sad'
                            elif score > 0.7:
                                emotion = 'Sad'
                            else:
                                emotion = 'Negative'
                        
                        results.append({
                            'timestamp': format_timestamp(start_time),
                            'start_seconds': round(start_time, 2),
                            'end_seconds': round(end_time, 2),
                            'text': text,
                            'emotion': emotion,
                            'confidence': round(score * 100, 2),
                            'sentiment': label
                        })
                        
                except sr.UnknownValueError:
                    # No speech detected in this chunk
                    continue
                except sr.RequestError as e:
                    print(f"Speech recognition error: {e}")
                    continue
                except Exception as e:
                    print(f"Error processing chunk: {e}")
                    continue
        
        # Clean up converted file if different from original
        if wav_path != audio_path and os.path.exists(wav_path):
            os.remove(wav_path)
        
        return {
            'success': True,
            'duration': round(duration, 2),
            'total_segments': len(results),
            'results': results,
            'emotion_summary': generate_emotion_summary(results)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def format_timestamp(seconds):
    """Format seconds to MM:SS format"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def generate_emotion_summary(results):
    """Generate summary statistics of emotions"""
    if not results:
        return {}
    
    emotion_counts = {}
    total_confidence = {}
    
    for result in results:
        emotion = result['emotion']
        confidence = result['confidence']
        
        if emotion in emotion_counts:
            emotion_counts[emotion] += 1
            total_confidence[emotion] += confidence
        else:
            emotion_counts[emotion] = 1
            total_confidence[emotion] = confidence
    
    summary = {}
    for emotion, count in emotion_counts.items():
        summary[emotion] = {
            'count': count,
            'percentage': round((count / len(results)) * 100, 2),
            'avg_confidence': round(total_confidence[emotion] / count, 2)
        }
    
    return summary

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle audio file upload and analysis"""
    try:
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file provided'})
        
        file = request.files['audio']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze audio
        result = analyze_audio_sentiment(filepath)
        
        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'sentiment_model_loaded': sentiment_analyzer is not None})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
