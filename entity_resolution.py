import os
import pandas as pd

def load_profiles():
    base_dir = os.getcwd()
    df = pd.read_csv(os.path.join(base_dir, 'student-or-staff-profiles.csv'))
    return df

def build_entity_table(profiles_df):
    keys = ['entity_id', 'student_id', 'staff_id', 'card_id', 'face_id', 'device_hash']
    entity_df = profiles_df[keys].copy()
    print("Missing values in entity identifiers:")
    print(entity_df.isnull().sum())
    return entity_df

if __name__ == "__main__":
    profiles = load_profiles()
    table = build_entity_table(profiles)
    print(table.head())
