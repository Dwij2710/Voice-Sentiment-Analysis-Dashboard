# Voice Sentiment Analysis Dashboard 🎤

A comprehensive web application that analyzes audio files to detect emotions and sentiment with precise timestamps. The app provides interactive visualizations showing when emotions change throughout the audio.

## Features

- **Real-time Emotion Detection**: Identifies emotions (Very Happy, Happy, Positive, Negative, Sad, Very Sad) at specific timestamps
- **Interactive Dashboard**: Beautiful charts and visualizations
- **Detailed Timeline**: Shows exactly at what minute and second each emotion is captured
- **Emotion Distribution**: Pie chart showing overall emotion breakdown
- **Timeline Chart**: Visual representation of emotion changes over time
- **Comprehensive Statistics**: Confidence scores, percentages, and summaries

## Technologies Used

- **Backend**: Flask, Python
- **Audio Processing**: Librosa, SpeechRecognition, Pydub
- **AI/ML**: Transformers (HuggingFace), DistilBERT for sentiment analysis
- **Frontend**: HTML, CSS, JavaScript
- **Visualization**: Chart.js (Flask version), Plotly (Streamlit version)

## Deployment Options

### Option 1: Deploy on Render (Flask Version)

1. **Create a GitHub Repository**
   - Create a new repository on GitHub
   - Upload all files from this project

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: voice-sentiment-app
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
   - Click "Create Web Service"

3. **Wait for Deployment**
   - Render will automatically build and deploy your app
   - You'll get a URL like: `https://voice-sentiment-app.onrender.com`

### Option 2: Deploy on Streamlit Cloud (Streamlit Version)

1. **Prepare Files**
   - Create a GitHub repository with `streamlit_app.py` and `requirements.txt`

2. **Deploy on Streamlit**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Set main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Access Your App**
   - You'll get a URL like: `https://your-app.streamlit.app`

### Option 3: Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Flask App**
   ```bash
   python app.py
   ```
   Access at: `http://localhost:5000`

3. **Or Run Streamlit App**
   ```bash
   streamlit run streamlit_app.py
   ```
   Access at: `http://localhost:8501`

## Usage

1. **Upload Audio File**
   - Click on the upload area
   - Select an audio file (MP3, WAV, M4A, OGG)
   - Max file size: 50MB

2. **Analyze**
   - Click "Analyze Audio" button
   - Wait for processing (may take 1-2 minutes depending on file length)

3. **View Results**
   - **Stats Dashboard**: Duration, segments analyzed, dominant emotion
   - **Emotion Distribution Chart**: Pie chart showing emotion breakdown
   - **Timeline Chart**: Line graph showing emotion changes over time
   - **Detailed Timeline**: Precise timestamps with transcribed text
   - **Emotion Summary**: Statistics for each detected emotion

## How It Works

1. **Audio Processing**: The app converts uploaded audio to WAV format
2. **Segmentation**: Audio is split into 3-second chunks
3. **Speech Recognition**: Google Speech Recognition transcribes each chunk
4. **Sentiment Analysis**: DistilBERT model analyzes sentiment of transcribed text
5. **Emotion Mapping**: Sentiment scores are mapped to emotion categories
6. **Visualization**: Results are displayed with timestamps and charts

## Emotion Categories

- **Very Happy**: Strong positive sentiment (>90% confidence)
- **Happy**: Positive sentiment (70-90% confidence)
- **Positive**: Mild positive sentiment (<70% confidence)
- **Negative**: Mild negative sentiment (<70% confidence)
- **Sad**: Negative sentiment (70-90% confidence)
- **Very Sad**: Strong negative sentiment (>90% confidence)

## Dashboard Components

### 1. Statistics Cards
- Total duration of audio
- Number of segments analyzed
- Dominant emotion detected

### 2. Emotion Distribution (Pie Chart)
- Visual breakdown of all emotions detected
- Percentages and counts

### 3. Timeline Chart
- X-axis: Time in seconds
- Y-axis: Emotion level
- Points colored by emotion type
- Hover to see transcribed text

### 4. Detailed Timeline
- Exact timestamps (MM:SS format)
- Transcribed text for each segment
- Emotion badge with color coding
- Confidence percentage

### 5. Emotion Summary
- Count of each emotion
- Percentage distribution
- Average confidence score

## Requirements

- Python 3.9+
- Internet connection (for Google Speech Recognition API)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## File Structure

```
voice-sentiment-app/
├── app.py                 # Flask application
├── streamlit_app.py       # Streamlit application
├── requirements.txt       # Python dependencies
├── Procfile              # Render deployment config
├── render.yaml           # Render configuration
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Stylesheet
│   └── js/
│       └── script.js     # Frontend JavaScript
└── README.md             # This file
```

## Limitations

- Audio files must be under 50MB
- Processing time depends on audio length (approx. 20-30 seconds per minute of audio)
- Requires internet connection for speech recognition
- Only supports languages supported by Google Speech Recognition
- Emotion detection accuracy depends on speech clarity and content

## Troubleshooting

**Issue**: "No speech detected"
- **Solution**: Ensure audio has clear speech, increase volume, or try a different file

**Issue**: Slow processing
- **Solution**: Longer audio files take more time; consider splitting large files

**Issue**: Deployment fails
- **Solution**: Check that all dependencies are in requirements.txt and Python version is 3.9+

## Future Enhancements

- Support for multiple languages
- Real-time audio recording
- Export results to PDF/CSV
- More emotion categories (anger, surprise, fear, etc.)
- Speaker diarization (multiple speakers)
- Batch processing of multiple files

## License

MIT License - feel free to use and modify for your projects!

## Support

For issues or questions, please create an issue in the GitHub repository.

---

Built with ❤️ using Flask, Streamlit, and AI
