import os
import pandas as pd

def load_data():
    base_dir = os.getcwd()
    profiles = pd.read_csv(os.path.join(base_dir, 'student-or-staff-profiles.csv'))
    card_swipes = pd.read_csv(os.path.join(base_dir, 'campus_card_swipes.csv'))
    return profiles, card_swipes

def build_entity_table(profiles):
    profiles['student_or_staff_id'] = profiles['student_id'].fillna(profiles['staff_id'])
    keys = ['entity_id', 'student_or_staff_id', 'card_id', 'face_id', 'device_hash']
    return profiles[keys]

def join_card_swipes(entity_table, card_swipes):
    return pd.merge(card_swipes, entity_table, on='card_id', how='left')

def load_wifi_logs():
    base_dir = os.getcwd()
    wifi_path = os.path.join(base_dir, 'wifi_associations_logs.csv')
    return pd.read_csv(wifi_path)

def join_wifi_logs(wifi_logs, entity_table):
    return pd.merge(wifi_logs, entity_table, on='device_hash', how='left')

if __name__ == "__main__":
    profiles, card_swipes = load_data()
    entity_table = build_entity_table(profiles)
    merged = join_card_swipes(entity_table, card_swipes)
    print(merged.head())
