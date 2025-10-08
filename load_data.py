import os
import pandas as pd

def load_dataset(file_name):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, file_name)
    print(f"Loading {file_name} from {path}")
    df = pd.read_csv(path)
    print(df.info())
    print(df.head())
    print("\n")
    return df

def load_linked_sources():
    """Load all linked data sources and return as tuples."""
    profiles = load_dataset('student-or-staff-profiles.csv')
    card_swipes = load_dataset('campus_card_swipes.csv')
    cctv = load_dataset('cctv_frames.csv')
    face_embeddings = load_dataset('face_embeddings.csv')
    free_text_notes = load_dataset('free_text_notes.csv')
    lab_bookings = load_dataset('lab_bookings.csv')
    library_checkouts = load_dataset('library_checkouts.csv')
    wifi_logs = load_dataset('wifi_associations_logs.csv')

    return (card_swipes, cctv, wifi_logs, lab_bookings,
            free_text_notes, library_checkouts, profiles)

def main():
    load_linked_sources()

if __name__ == "__main__":
    main()
