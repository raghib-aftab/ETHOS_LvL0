import os
import pandas as pd

def load_dataset(file_name):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, 'data', file_name)
    print(f"Loading {file_name} from {path}")
    df = pd.read_csv(path)
    print(df.info())
    print(df.head())
    print("\n")
    return df

def load_linked_sources():
    """Load all linked data sources and return as tuples."""
    profiles = load_dataset('data/student-or-staff-profiles.csv')
    card_swipes = load_dataset('data/campus_card_swipes.csv')
    cctv = load_dataset('data/cctv_frames.csv')
    face_embeddings = load_dataset('data/face_embeddings.csv')
    free_text_notes = load_dataset('data/free_text_notes.csv')
    lab_bookings = load_dataset('data/lab_bookings.csv')
    library_checkouts = load_dataset('data/library_checkouts.csv')
    wifi_logs = load_dataset('data/wifi_associations_logs.csv')

    return (card_swipes, cctv, wifi_logs, lab_bookings,
            free_text_notes, library_checkouts, profiles)

def main():
    load_linked_sources()

if __name__ == "__main__":
    main()
