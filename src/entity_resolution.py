from load_data import load_linked_sources

def build_entity_table(profiles_df):
    """
    Create unified entity table with key identifiers.
    """
    keys = ['entity_id', 'student_id', 'staff_id', 'card_id', 'face_id', 'device_hash']
    entity_df = profiles_df[keys].copy()
    return entity_df

def resolve_entity(entity_df, card_id=None, face_id=None, device_hash=None, student_id=None, staff_id=None):
    """
    Resolve canonical entity_id given any identifier.
    """
    for col, val in [
        ('card_id', card_id),
        ('face_id', face_id),
        ('device_hash', device_hash),
        ('student_id', student_id),
        ('staff_id', staff_id),
    ]:
        if val is not None:
            found = entity_df[entity_df[col] == val]
            if not found.empty:
                return found.iloc[0]['entity_id']
    return None

def print_resolved_entities(entity_df):
    """
    Print resolved entities clearly without printing loaded data content.
    """
    print("--- Resolved Entities ---")
    id_types = ['card_id', 'face_id', 'device_hash', 'student_id', 'staff_id']
    for id_type in id_types:
        values = entity_df[id_type].dropna().unique()
        if values.size == 0:
            print(f"No values found for identifier: {id_type}")
            continue
        print(f"\nIdentifier Type: {id_type}")
        print(f"Total unique IDs: {len(values)}")
        # Print resolution for first 5 sample IDs
        print(f"Sample resolved entities for first 5 {id_type}s:")
        for val in values[:5]:
            entity_id = resolve_entity(entity_df, **{id_type: val})
            print(f"  {id_type}: {val}  -->  entity_id: {entity_id}")

def main():
    # Load all linked sources; get profiles last
    _, _, _, _, _, _, profiles = load_linked_sources()
    entity_table = build_entity_table(profiles)
    print_resolved_entities(entity_table)

if __name__ == "__main__":
    main()
