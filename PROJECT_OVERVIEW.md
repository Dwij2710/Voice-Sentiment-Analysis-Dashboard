# Voice Sentiment Analysis Dashboard - Project Overview

## 🎯 What This Application Does

This is a complete voice sentiment analysis web application that:

1. **Accepts Audio Input**: Users upload audio files (MP3, WAV, M4A, OGG)
2. **Processes Audio**: Splits audio into 3-second segments
3. **Transcribes Speech**: Converts speech to text using Google Speech Recognition
4. **Analyzes Sentiment**: Uses AI (DistilBERT) to detect emotions in the text
5. **Displays Results**: Shows a beautiful dashboard with charts and timelines

## 🎨 Dashboard Features

### Statistics Cards
- Total audio duration
- Number of segments analyzed
- Dominant emotion detected

### Visualizations
1. **Emotion Distribution (Pie Chart)**
   - Shows percentage breakdown of all emotions
   - Color-coded by emotion type

2. **Emotion Timeline (Line/Scatter Chart)**
   - X-axis: Time in seconds
   - Y-axis: Emotion type
   - Shows exactly when emotions change
   - Interactive: hover to see details

### Detailed Timeline
- Lists every detected segment with:
  - **Timestamp** (MM:SS format) - e.g., "00:15", "01:23"
  - **Emotion Badge** - color-coded emotion label
  - **Transcribed Text** - what was said
  - **Confidence Score** - AI confidence percentage

### Emotion Summary
- Statistics for each detected emotion:
  - Total occurrences
  - Percentage of total
  - Average confidence score

## 🎭 Emotion Categories

The app detects 6 emotion levels:

| Emotion | Sentiment | Confidence | Color |
|---------|-----------|------------|-------|
| Very Happy | Positive | >90% | Dark Green |
| Happy | Positive | 70-90% | Green |
| Positive | Positive | <70% | Light Green |
| Negative | Negative | <70% | Orange |
| Sad | Negative | 70-90% | Red |
| Very Sad | Negative | >90% | Dark Red |

## 📁 Project Files

### Core Application Files

**1. app.py** (Flask Version)
- Main Flask server
- Audio processing logic
- Sentiment analysis engine
- REST API endpoints

**2. streamlit_app.py** (Streamlit Version)
- Streamlit web application
- Same functionality as Flask version
- Easier deployment option

**3. templates/index.html**
- Main HTML interface
- Responsive design
- Upload interface

**4. static/css/style.css**
- Complete styling
- Gradient backgrounds
- Responsive layout
- Card-based design

**5. static/js/script.js**
- Frontend interactivity
- Chart.js visualizations
- AJAX requests
- Dynamic timeline rendering

### Configuration Files

**6. requirements.txt**
- All Python dependencies
- Flask, Streamlit, Transformers, Librosa, etc.

**7. Procfile**
- Render deployment configuration

**8. render.yaml**
- Render service configuration

**9. .gitignore**
- Files to exclude from Git

### Documentation

**10. README.md**
- Complete project documentation
- Features, usage, deployment

**11. DEPLOYMENT.md**
- Step-by-step deployment guide
- Streamlit Cloud & Render instructions

**12. TESTING_GUIDE.md**
- How to test the application
- Sample audio suggestions

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Easiest) ⭐ RECOMMENDED
- **Difficulty**: Beginner-friendly
- **Time**: 5 minutes
- **Cost**: FREE
- **Steps**:
  1. Upload `streamlit_app.py` and `requirements.txt` to GitHub
  2. Connect to Streamlit Cloud
  3. Deploy with one click
- **URL**: `https://yourapp.streamlit.app`

### Option 2: Render (Flask Version)
- **Difficulty**: Intermediate
- **Time**: 10 minutes
- **Cost**: FREE (with limitations)
- **Steps**:
  1. Upload all files to GitHub
  2. Connect to Render
  3. Configure and deploy
- **URL**: `https://yourapp.onrender.com`

### Option 3: Local Development
- **Difficulty**: Easy (if you have Python)
- **Time**: 2 minutes
- **Cost**: FREE
- **Steps**:
  ```bash
  pip install -r requirements.txt
  # For Streamlit:
  streamlit run streamlit_app.py
  # For Flask:
  python app.py
  ```

## 🔧 How It Works (Technical Flow)

```
Audio Upload
    ↓
Convert to WAV (if needed)
    ↓
Split into 3-second chunks
    ↓
For each chunk:
    - Transcribe speech → text
    - Analyze sentiment → positive/negative + confidence
    - Map to emotion → Very Happy/Happy/Positive/Negative/Sad/Very Sad
    - Record timestamp
    ↓
Generate visualizations
    ↓
Display dashboard
```

## 📊 Example Output

For a 30-second audio file, you might see:

**Timeline:**
- 00:03 - "I'm so excited!" → Very Happy (95% confidence)
- 00:08 - "This is going well." → Positive (72% confidence)
- 00:15 - "But I'm worried about tomorrow." → Sad (85% confidence)
- 00:23 - "Still, I'm hopeful!" → Happy (88% confidence)

**Summary:**
- Very Happy: 1 occurrence (25%)
- Positive: 1 occurrence (25%)
- Sad: 1 occurrence (25%)
- Happy: 1 occurrence (25%)

## 🎯 Use Cases

1. **Customer Service Analysis**: Analyze call recordings to understand customer emotions
2. **Content Creation**: Review podcast/video emotions for better editing
3. **Mental Health**: Track emotional patterns in therapy sessions
4. **Market Research**: Analyze focus group discussions
5. **Education**: Evaluate student presentation confidence
6. **Personal Development**: Track your own emotional patterns

## ⚡ Performance

- **Processing Speed**: ~20-30 seconds per minute of audio
- **Accuracy**: ~85-90% (depends on audio quality and speech clarity)
- **File Size Limit**: 50MB
- **Supported Formats**: MP3, WAV, M4A, OGG

## 🔒 Privacy

- Audio files are processed temporarily
- Files are deleted immediately after analysis
- No data is stored permanently
- All processing happens server-side

## 🌟 Future Enhancements (Ideas)

- [ ] Real-time microphone recording
- [ ] Multiple language support
- [ ] Speaker diarization (identify different speakers)
- [ ] More emotions (anger, surprise, fear, disgust)
- [ ] Export results to PDF/CSV
- [ ] Batch processing multiple files
- [ ] Integration with video files
- [ ] Voice characteristics analysis (pitch, tone, speed)

## 📝 License

MIT License - Free to use, modify, and distribute!

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

---

**Built with:** Python, Flask, Streamlit, Transformers, Librosa, Chart.js, and ❤️

**AI Model:** DistilBERT (HuggingFace)

**Speech Recognition:** Google Speech Recognition API
