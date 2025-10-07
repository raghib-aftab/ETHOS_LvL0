import os
import pandas as pd

def load_dataset(file_name):
    base_dir = os.getcwd()
    path = os.path.join(base_dir, file_name)
    df = pd.read_csv(path)
    print(f"Loaded {file_name}, {len(df)} rows")
    return df

if __name__ == "__main__":
    files = [
        'student-or-staff-profiles.csv',
        'campus_card_swipes.csv',
        'cctv_frames.csv',
        'face embeddings.csv',
        'free_text_notes.csv',
        'lab_bookings.csv',
        'library_checkouts.csv',
        'wifi_associations_logs.csv'
    ]
    for f in files:
        load_dataset(f)
