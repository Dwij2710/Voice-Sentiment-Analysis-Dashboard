# 🚀 Quick Deployment Guide

## Fastest Deployment: Streamlit Cloud (Recommended)

### Steps:

1. **Create GitHub Account** (if you don't have one)
   - Go to github.com and sign up

2. **Create New Repository**
   - Click "+" → "New repository"
   - Name it: `voice-sentiment-app`
   - Make it Public
   - Click "Create repository"

3. **Upload Files**
   - Click "uploading an existing file"
   - Upload these files:
     - `streamlit_app.py`
     - `requirements.txt`
   - Click "Commit changes"

4. **Deploy on Streamlit**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file path: `streamlit_app.py`
   - Click "Deploy!"

5. **Done! 🎉**
   - Wait 2-3 minutes for deployment
   - You'll get a public URL like: `https://yourapp.streamlit.app`
   - Share this URL with anyone!

---

## Alternative: Render (Flask Version)

### Steps:

1. **Create GitHub Repository** (same as above)
   - Upload ALL files from the project folder

2. **Sign Up on Render**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

3. **Create Web Service (The Easy Way)**
   - Go to [dashboard.render.com](https://dashboard.render.com)
   - Click "New +" → "**Blueprint**"
   - Connect your GitHub repository `Voice-Sentiment-Analysis-Dashboard`
   - Render will automatically detect the `render.yaml` file.
   - Click "Apply" to start the deployment.

4. **Wait for Deployment**
   - It will take a few minutes to build and install dependencies.
   - Once finished, you will see a green "Live" badge.
   - Your URL will be shown at the top (e.g., `https://speech-emotion-monitor-xxxx.onrender.com`).

> [!WARNING]
> **Free Tier Limits**: Render's free tier has 512MB RAM. If the deployment fails with an "Out of Memory" error, it's because the AI models (Torch/Transformers) are too large. You may need to upgrade to a paid starter plan ($7/mo) or use a smaller model.

---

## Testing Locally First

### Prerequisites:
- Python 3.9 or higher installed
- pip installed

### For Streamlit:
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

### For Flask:
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

---

## Need Help?

- **Streamlit**: https://docs.streamlit.io/streamlit-community-cloud/get-started
- **Render**: https://render.com/docs
- **GitHub**: https://docs.github.com/en/get-started/quickstart

---

**Tip**: Streamlit is easier and faster for deployment. Use Flask/Render if you need more control.
