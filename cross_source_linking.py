import os
import pandas as pd

def load_data():
    base_dir = os.getcwd()
    profiles_path = os.path.join(base_dir, 'student-or-staff-profiles.csv')
    card_swipes_path = os.path.join(base_dir, 'campus_card_swipes.csv')

    profiles = pd.read_csv(profiles_path)
    card_swipes = pd.read_csv(card_swipes_path)
    return profiles, card_swipes

def build_entity_table(profiles):
    profiles['student_or_staff_id'] = profiles['student_id'].fillna(profiles['staff_id'])
    keys = ['entity_id', 'student_or_staff_id', 'card_id', 'face_id', 'device_hash']
    return profiles[keys]

def join_card_swipes(entity_table, card_swipes):
    return pd.merge(card_swipes, entity_table, on='card_id', how='left')

def load_cctv_and_faces():
    base_dir = os.getcwd()
    cctv_path = os.path.join(base_dir, 'cctv_frames.csv')
    faces_path = os.path.join(base_dir, 'face_embeddings.csv')
    cctv = pd.read_csv(cctv_path)
    faces = pd.read_csv(faces_path)
    return cctv, faces

def join_cctv_with_faces(cctv, faces):
    faces['face_id'] = faces['face_id'].str.replace('.jpg', '', regex=False)
    return pd.merge(cctv, faces, on='face_id', how='left')

def join_with_entities(cctv_faces, entity_table):
    return pd.merge(cctv_faces, entity_table, on='face_id', how='left')

def load_wifi_logs():
    base_dir = os.getcwd()
    wifi_path = os.path.join(base_dir, 'wifi_associations_logs.csv')
    return pd.read_csv(wifi_path)

def join_wifi_logs(wifi_logs, entity_table):
    return pd.merge(wifi_logs, entity_table, on='device_hash', how='left')

def load_lab_bookings():
    base_dir = os.getcwd()
    lab_path = os.path.join(base_dir, 'lab_bookings.csv')
    return pd.read_csv(lab_path)

def join_lab_bookings(lab_bookings, entity_table):
    return pd.merge(lab_bookings, entity_table, on='entity_id', how='left')

def load_text_notes():
    base_dir = os.getcwd()
    notes_path = os.path.join(base_dir, 'free_text_notes.csv')
    return pd.read_csv(notes_path)

def join_text_notes(text_notes, entity_table):
    return pd.merge(text_notes, entity_table, on='entity_id', how='left')

def load_library_checkouts():
    base_dir = os.getcwd()
    library_path = os.path.join(base_dir, 'library_checkouts.csv')
    return pd.read_csv(library_path)

def join_library_checkouts(library_checkouts, entity_table):
    return pd.merge(library_checkouts, entity_table, on='entity_id', how='left')

def main():
    profiles, card_swipes = load_data()
    entity_table = build_entity_table(profiles)

    merged_card_swipes = join_card_swipes(entity_table, card_swipes)

    cctv, faces = load_cctv_and_faces()
    cctv_faces = join_cctv_with_faces(cctv, faces)
    merged_cctv_faces = join_with_entities(cctv_faces, entity_table)

    wifi_logs = load_wifi_logs()
    merged_wifi_logs = join_wifi_logs(wifi_logs, entity_table)

    lab_bookings = load_lab_bookings()
    merged_lab_bookings = join_lab_bookings(lab_bookings, entity_table)

    text_notes = load_text_notes()
    merged_text_notes = join_text_notes(text_notes, entity_table)

    library_checkouts = load_library_checkouts()
    merged_library_checkouts = join_library_checkouts(library_checkouts, entity_table)

    print("Sample linked card swipes with profiles:")
    print(merged_card_swipes.head(5))
    print("\nSample linked CCTV and face embeddings with profiles:")
    print(merged_cctv_faces.head(5))
    print("\nSample linked Wi-Fi logs with profiles:")
    print(merged_wifi_logs.head(5))
    print("\nSample linked Lab bookings with profiles:")
    print(merged_lab_bookings.head(5))
    print("\nSample linked Free text notes with profiles:")
    print(merged_text_notes.head(5))
    print("\nSample linked Library checkouts with profiles:")
    print(merged_library_checkouts.head(5))

if __name__ == "__main__":
    main()
