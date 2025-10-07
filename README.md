# Streamlit Activity Timeline - Root Version

## 🚀 How to Deploy on Streamlit Cloud
1. Push all these files to your GitHub repository root.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) → New app.
3. Set main file path to:
   ```
   app_streamlit.py
   ```
4. Click **Deploy**.

## 📂 Data Files
All CSVs are placed in the repo root. The app will auto-detect them.
If `face_embeddings.csv` is missing, it will be downloaded automatically from Google Drive.

## ✅ Requirements
- Python 3.9+
- streamlit, pandas, plotly, gdown
