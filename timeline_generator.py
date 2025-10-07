import os
import pandas as pd
import streamlit as st

def load_or_upload_csv(name, path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        uploaded = st.file_uploader(f"Upload {name}", type=["csv"])
        if uploaded is not None:
            return pd.read_csv(uploaded)
        st.warning(f"{name} not found. Please upload it.")
        return pd.DataFrame()

def load_face_embeddings(drive_folder_id='1510SDJg3pohua-0sP6ZMbmJj4RGKZQdw'):
    import gdown
    local_path = 'face_embeddings.csv'
    if not os.path.exists(local_path):
        try:
            st.info("Downloading face_embeddings.csv from Google Drive...")
            gdown.download_folder(url=f"https://drive.google.com/drive/folders/{drive_folder_id}", output='.', quiet=False, use_cookies=False)
        except Exception as e:
            st.error(f"Failed to download embeddings from Google Drive: {e}")
    if os.path.exists(local_path):
        return pd.read_csv(local_path)
    else:
        st.warning("face_embeddings.csv not found or failed to download.")
        return pd.DataFrame()

def load_linked_sources():
    files = {
        "card_swipes": "campus_card_swipes.csv",
        "cctv": "cctv_frames.csv",
        "wifi_logs": "wifi_associations_logs.csv",
        "lab_bookings": "lab_bookings.csv",
        "text_notes": "free_text_notes.csv",
        "library_checkouts": "library_checkouts.csv",
        "entity_table": "student-or-staff-profiles.csv",
    }

    dataframes = {}
    for key, filename in files.items():
        dataframes[key] = load_or_upload_csv(filename, filename)

    embeddings = load_face_embeddings()

    return (
        dataframes["card_swipes"],
        dataframes["cctv"],
        dataframes["wifi_logs"],
        dataframes["lab_bookings"],
        dataframes["text_notes"],
        dataframes["library_checkouts"],
        dataframes["entity_table"],
        embeddings
    )

def generate_timeline(entity_id, *args, **kwargs):
    st.write(f"Generating timeline for {entity_id}... (placeholder logic)")
    timeline = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=5, freq="D"),
        "event": ["Swipe", "WiFi", "CCTV", "Library", "Lab"]
    })
    event_counts = timeline["event"].value_counts().to_dict()
    inactivity_flag = False
    predicted_next = "Library"
    anomalies = []
    return timeline, event_counts, inactivity_flag, predicted_next, anomalies

def visualize_timeline(timeline, entity_id):
    import plotly.express as px
    if timeline.empty:
        return None
    fig = px.timeline(timeline, x_start="timestamp", x_end="timestamp", y="event",
                      title=f"Timeline for {entity_id}")
    return fig
