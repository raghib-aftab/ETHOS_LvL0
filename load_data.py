import os
import pandas as pd

def load_dataset(file_name):
    # Dynamically get absolute path to the 'data' folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, 'data', file_name)
    print(f"Loading {file_name} from {path}")
    df = pd.read_csv(path)
    print(df.info())
    print(df.head())
    print("\n")
    return df

def main():
    dataset_files = [
        'student-or-staff-profiles.csv',
        'campus_card_swipes.csv',
        'cctv_frames.csv',
        'face_embeddings.csv',
        'free_text_notes.csv',
        'lab_bookings.csv',
        'library_checkouts.csv',
        'wifi_associations_logs.csv'
    ]
    data = {}
    for file_name in dataset_files:
        data[file_name] = load_dataset(file_name)

if __name__ == "__main__":
    main()
