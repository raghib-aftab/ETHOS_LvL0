from load_data import load_linked_sources
from entity_resolution import build_entity_table
import pandas as pd
import os

def report_link_stats(df, join_col, source_name):
    total = len(df)
    matched = df[join_col].notnull().sum()
    unmatched = total - matched
    print(f"\n{source_name} Link Stats:")
    print(f"  Total records       : {total}")
    print(f"  Records linked to entity_id : {matched} ({matched / total:.2%})")
    print(f"  Records unmatched   : {unmatched} ({unmatched / total:.2%})")
    # Show sample of unmatched join keys if any
    if unmatched > 0:
        unmatched_samples = df[df[join_col].isnull()].head(3)
        print(f"  Sample unmatched records (up to 3 shown):")
        print(unmatched_samples)

def cross_source_linking():
    # Load datasets without printing CSV details
    card_swipes, cctv, wifi_logs, lab_bookings, free_text_notes, library_checkouts, profiles = load_linked_sources()

    # Build unified entity table
    entity_table = build_entity_table(profiles)

    # Join Card Swipes
    merged_card_swipes = pd.merge(card_swipes, entity_table, on='card_id', how='left')
    report_link_stats(merged_card_swipes, 'entity_id', 'Card Swipes')

    # Load faces and strip '.jpg'
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    faces_path = os.path.join(base_dir, 'data', 'face_embeddings.csv')
    faces = pd.read_csv(faces_path)
    faces['face_id'] = faces['face_id'].str.replace('.jpg', '', regex=False)

    # Join CCTV and Faces
    cctv_faces = pd.merge(cctv, faces, on='face_id', how='left')
    merged_cctv_faces = pd.merge(cctv_faces, entity_table, on='face_id', how='left')
    report_link_stats(merged_cctv_faces, 'entity_id', 'CCTV + Face Embeddings')

    # Join Wi-Fi Logs
    merged_wifi_logs = pd.merge(wifi_logs, entity_table, on='device_hash', how='left')
    report_link_stats(merged_wifi_logs, 'entity_id', 'Wi-Fi Logs')

    # Join Lab Bookings
    merged_lab_bookings = pd.merge(lab_bookings, entity_table, on='entity_id', how='left')
    report_link_stats(merged_lab_bookings, 'entity_id', 'Lab Bookings')

    # Join Text Notes
    merged_text_notes = pd.merge(free_text_notes, entity_table, on='entity_id', how='left')
    report_link_stats(merged_text_notes, 'entity_id', 'Free Text Notes')

    # Join Library Checkouts
    merged_library_checkouts = pd.merge(library_checkouts, entity_table, on='entity_id', how='left')
    report_link_stats(merged_library_checkouts, 'entity_id', 'Library Checkouts')

    # Print Sample Records for Review
    print("\n--- Sample Linked Records (up to 5 from each) ---")
    print("\nCard Swipes:")
    print(merged_card_swipes.head(5))

    print("\nCCTV + Face Embeddings:")
    print(merged_cctv_faces.head(5))

    print("\nWi-Fi Logs:")
    print(merged_wifi_logs.head(5))

    print("\nLab Bookings:")
    print(merged_lab_bookings.head(5))

    print("\nFree Text Notes:")
    print(merged_text_notes.head(5))

    print("\nLibrary Checkouts:")
    print(merged_library_checkouts.head(5))

    return {
        'card_swipes': merged_card_swipes,
        'cctv_faces': merged_cctv_faces,
        'wifi_logs': merged_wifi_logs,
        'lab_bookings': merged_lab_bookings,
        'text_notes': merged_text_notes,
        'library_checkouts': merged_library_checkouts
    }

def main():
    cross_source_linking()

if __name__ == '__main__':
    main()
