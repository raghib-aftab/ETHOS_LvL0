import os
import pandas as pd

def load_profiles():
    base_dir = os.getcwd()
    data_path = os.path.join(base_dir, 'student-or-staff-profiles.csv')
    print(f"Loading data from: {data_path}")
    df = pd.read_csv(data_path)
    return df

def build_entity_table(profiles_df):
    keys = ['entity_id', 'student_id', 'staff_id', 'card_id', 'face_id', 'device_hash']
    entity_df = profiles_df[keys].copy()

    print("Missing values in entity identifiers:")
    print(entity_df.isnull().sum())
    return entity_df

def main():
    profiles = load_profiles()
    entity_table = build_entity_table(profiles)
    print("\nUnified Entity Table Sample:")
    print(entity_table.head(10))

if __name__ == "__main__":
    main()
