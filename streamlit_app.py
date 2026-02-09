import streamlit as st
import librosa
import numpy as np
from transformers import pipeline
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Voice Sentiment Analysis",
    page_icon="🎤",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    h1 {
        color: #667eea;
        text-align: center;
    }
    .emotion-card {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 5px solid;
    }
</style>
""", unsafe_allow_html=True)

# Initialize sentiment analyzer
@st.cache_resource
def load_sentiment_model():
    try:
        return pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=-1
        )
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def convert_to_wav(audio_path):
    """Convert audio file to WAV format"""
    try:
        audio = AudioSegment.from_file(audio_path)
        wav_path = audio_path.rsplit('.', 1)[0] + '_converted.wav'
        audio.export(wav_path, format='wav')
        return wav_path
    except Exception as e:
        st.error(f"Error converting audio: {e}")
        return audio_path

def analyze_audio_sentiment(audio_path, sentiment_analyzer):
    """Analyze sentiment from audio file"""
    results = []
    
    try:
        # Convert to WAV
        wav_path = convert_to_wav(audio_path)
        
        # Load audio
        audio, sr_rate = librosa.load(wav_path, sr=16000)
        duration = librosa.get_duration(y=audio, sr=sr_rate)
        
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Process in chunks
        chunk_duration = 3.0
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with sr.AudioFile(wav_path) as source:
            total_chunks = int(duration / chunk_duration) + 1
            
            for i, start_time in enumerate(np.arange(0, duration, chunk_duration)):
                end_time = min(start_time + chunk_duration, duration)
                
                progress_bar.progress((i + 1) / total_chunks)
                status_text.text(f"Processing segment {i+1} of {total_chunks}...")
                
                try:
                    recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio_chunk = recognizer.record(source, duration=chunk_duration)
                    
                    # Transcribe
                    text = recognizer.recognize_google(audio_chunk)
                    
                    if text and sentiment_analyzer:
                        # Analyze sentiment
                        sentiment = sentiment_analyzer(text[:512])[0]
                        label = sentiment['label']
                        score = sentiment['score']
                        
                        # Map to emotion
                        if label == 'POSITIVE':
                            if score > 0.9:
                                emotion = 'Very Happy'
                            elif score > 0.7:
                                emotion = 'Happy'
                            else:
                                emotion = 'Positive'
                        else:
                            if score > 0.9:
                                emotion = 'Very Sad'
                            elif score > 0.7:
                                emotion = 'Sad'
                            else:
                                emotion = 'Negative'
                        
                        results.append({
                            'timestamp': f"{int(start_time//60):02d}:{int(start_time%60):02d}",
                            'start_seconds': round(start_time, 2),
                            'end_seconds': round(end_time, 2),
                            'text': text,
                            'emotion': emotion,
                            'confidence': round(score * 100, 2),
                            'sentiment': label
                        })
                        
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    continue
        
        progress_bar.empty()
        status_text.empty()
        
        # Clean up
        if wav_path != audio_path and os.path.exists(wav_path):
            os.remove(wav_path)
        
        return results, duration
        
    except Exception as e:
        st.error(f"Error analyzing audio: {e}")
        return [], 0

def generate_emotion_summary(results):
    """Generate emotion statistics"""
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

# Main app
st.title("🎤 Voice Sentiment Analysis Dashboard")
st.markdown("Upload an audio file to analyze emotions and sentiment with precise timestamps")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info("""
    This app analyzes audio files and identifies emotions at specific timestamps.
    
    **Features:**
    - Emotion detection with timestamps
    - Interactive visualizations
    - Detailed timeline
    - Emotion distribution analysis
    """)
    
    st.header("Supported Formats")
    st.markdown("- MP3\n- WAV\n- M4A\n- OGG")

# File upload
uploaded_file = st.file_uploader("Choose an audio file", type=['mp3', 'wav', 'm4a', 'ogg'])

if uploaded_file is not None:
    # Save uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    
    # Analyze button
    if st.button("Analyze Audio", type="primary"):
        sentiment_analyzer = load_sentiment_model()
        
        if sentiment_analyzer:
            with st.spinner("Analyzing audio... This may take a minute."):
                results, duration = analyze_audio_sentiment(tmp_path, sentiment_analyzer)
            
            if results:
                # Display stats
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Duration", f"{int(duration//60)}:{int(duration%60):02d}")
                
                with col2:
                    st.metric("Segments Analyzed", len(results))
                
                with col3:
                    summary = generate_emotion_summary(results)
                    dominant = max(summary.items(), key=lambda x: x[1]['count'])[0] if summary else "N/A"
                    st.metric("Dominant Emotion", dominant)
                
                # Charts
                st.header("Visualizations")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Pie chart
                    emotion_counts = {emotion: stats['count'] for emotion, stats in summary.items()}
                    fig_pie = px.pie(
                        values=list(emotion_counts.values()),
                        names=list(emotion_counts.keys()),
                        title="Emotion Distribution",
                        color_discrete_sequence=px.colors.qualitative.Set2
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with col2:
                    # Timeline chart
                    emotion_map = {
                        'Very Sad': 1, 'Sad': 2, 'Negative': 3,
                        'Positive': 4, 'Happy': 5, 'Very Happy': 6
                    }
                    
                    df = pd.DataFrame(results)
                    df['emotion_value'] = df['emotion'].map(emotion_map)
                    
                    fig_timeline = px.scatter(
                        df,
                        x='start_seconds',
                        y='emotion_value',
                        color='emotion',
                        title="Emotion Timeline",
                        labels={'start_seconds': 'Time (seconds)', 'emotion_value': 'Emotion'},
                        hover_data=['text', 'confidence']
                    )
                    
                    fig_timeline.update_yaxis(
                        tickmode='array',
                        tickvals=list(emotion_map.values()),
                        ticktext=list(emotion_map.keys())
                    )
                    
                    st.plotly_chart(fig_timeline, use_container_width=True)
                
                # Detailed timeline
                st.header("Detailed Timeline")
                
                for result in results:
                    emotion_colors = {
                        'Very Happy': '#2e7d32', 'Happy': '#4caf50', 'Positive': '#8bc34a',
                        'Negative': '#ff9800', 'Sad': '#f44336', 'Very Sad': '#c62828'
                    }
                    
                    st.markdown(f"""
                    <div class="emotion-card" style="border-color: {emotion_colors.get(result['emotion'], '#999')}">
                        <strong>{result['timestamp']}</strong> - 
                        <span style="background: {emotion_colors.get(result['emotion'], '#999')}; 
                              color: white; padding: 2px 10px; border-radius: 10px;">
                            {result['emotion']}
                        </span>
                        <p>"{result['text']}"</p>
                        <small>Confidence: {result['confidence']}%</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Emotion summary
                st.header("Emotion Summary")
                
                cols = st.columns(len(summary))
                for idx, (emotion, stats) in enumerate(summary.items()):
                    with cols[idx]:
                        st.subheader(emotion)
                        st.write(f"**Occurrences:** {stats['count']}")
                        st.write(f"**Percentage:** {stats['percentage']}%")
                        st.write(f"**Avg Confidence:** {stats['avg_confidence']}%")
            else:
                st.warning("No speech detected in the audio file. Please try another file.")
        else:
            st.error("Failed to load sentiment analysis model.")
    
    # Clean up
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
