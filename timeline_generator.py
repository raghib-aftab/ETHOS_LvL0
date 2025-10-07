import os
import pandas as pd
import plotly.express as px
from collections import defaultdict

def load_linked_sources():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    card_swipes = pd.read_csv(os.path.join(base_dir, 'data', 'campus_card_swipes.csv'))
    cctv = pd.read_csv(os.path.join(base_dir, 'data', 'cctv_frames.csv'))
    wifi_logs = pd.read_csv(os.path.join(base_dir, 'data', 'wifi_associations_logs.csv'))
    lab_bookings = pd.read_csv(os.path.join(base_dir, 'data', 'lab_bookings.csv'))
    text_notes = pd.read_csv(os.path.join(base_dir, 'data', 'free_text_notes.csv'))
    library_checkouts = pd.read_csv(os.path.join(base_dir, 'data', 'library_checkouts.csv'))
    profiles = pd.read_csv(os.path.join(base_dir, 'data', 'student-or-staff-profiles.csv'))

    profiles['student_or_staff_id'] = profiles['student_id'].fillna(profiles['staff_id'])
    keys = ['entity_id', 'student_or_staff_id', 'card_id', 'face_id', 'device_hash']
    entity_table = profiles[keys]

    return (card_swipes, cctv, wifi_logs, lab_bookings, text_notes,
            library_checkouts, entity_table)

def build_transition_matrix(timeline):
    timeline = timeline.sort_values('timestamp')
    timeline = timeline.dropna(subset=['location'])

    transitions = defaultdict(lambda: defaultdict(int))

    prev_loc = None
    for loc in timeline['location']:
        if prev_loc:
            transitions[prev_loc][loc] += 1
        prev_loc = loc

    transition_matrix = {}
    for from_loc, to_dict in transitions.items():
        total = sum(to_dict.values())
        transition_matrix[from_loc] = {to_loc: count / total for to_loc, count in to_dict.items()}
    return transition_matrix

def predict_next_location(transition_matrix, current_location):
    if current_location not in transition_matrix:
        return None
    next_locations = transition_matrix[current_location]
    return max(next_locations, key=next_locations.get)

def anomaly_detection(timeline):
    anomalies = []

    gaps = timeline['timestamp'].diff().dt.days.fillna(0)
    large_gaps = timeline[gaps > 14]
    for idx, row in large_gaps.iterrows():
        anomalies.append(f"Inactivity gap of {int(gaps[idx])} days before {row['timestamp'].date()}")

    seen_locations = set()
    for idx, loc in enumerate(timeline['location']):
        if pd.isna(loc): 
            continue
        if loc not in seen_locations and len(seen_locations) > 0:
            anomalies.append(f"Visited new location: {loc} at {timeline.loc[idx, 'timestamp']}")
        seen_locations.add(loc)

    timeline['date'] = timeline['timestamp'].dt.date
    daily_counts = timeline.groupby('date').size()
    if len(daily_counts) > 1:
        mean = daily_counts.mean()
        std = daily_counts.std()
        for date, count in daily_counts.items():
            if abs(count - mean) > 2 * std:
                anomalies.append(f"Unusual activity count {count} on {date}")

    seen = set()
    unique_anomalies = []
    for a in anomalies:
        if a not in seen:
            seen.add(a)
            unique_anomalies.append(a)

    return unique_anomalies

def generate_timeline(entity_id, card_swipes, cctv, wifi_logs, lab_bookings,
                      text_notes, library_checkouts, entity_table,
                      start_date=None, end_date=None, event_types=None):
    card_swipes = pd.merge(card_swipes, entity_table[['entity_id', 'card_id']], on='card_id', how='left')
    card_swipes_filtered = card_swipes[card_swipes['entity_id'] == entity_id].copy()
    card_swipes_filtered['event_type'] = 'card_swipe'
    card_swipes_filtered['timestamp'] = pd.to_datetime(card_swipes_filtered['timestamp'])

    cctv = pd.merge(cctv, entity_table[['entity_id', 'face_id']], on='face_id', how='left')
    cctv_filtered = cctv[cctv['entity_id'] == entity_id].copy()
    cctv_filtered['event_type'] = 'cctv_sighting'
    cctv_filtered['timestamp'] = pd.to_datetime(cctv_filtered['timestamp'])

    wifi_logs = pd.merge(wifi_logs, entity_table[['entity_id', 'device_hash']], on='device_hash', how='left')
    wifi_filtered = wifi_logs[wifi_logs['entity_id'] == entity_id].copy()
    wifi_filtered['event_type'] = 'wifi_log'
    wifi_filtered['timestamp'] = pd.to_datetime(wifi_filtered['timestamp'])

    lab_filtered = lab_bookings[lab_bookings['entity_id'] == entity_id].copy()
    lab_filtered['event_type'] = 'lab_booking'
    lab_filtered['timestamp'] = pd.to_datetime(lab_filtered['start_time'])

    notes_filtered = text_notes[text_notes['entity_id'] == entity_id].copy()
    notes_filtered['event_type'] = 'text_note'
    notes_filtered['timestamp'] = pd.to_datetime(notes_filtered['timestamp'])

    library_filtered = library_checkouts[library_checkouts['entity_id'] == entity_id].copy()
    library_filtered['event_type'] = 'library_checkout'
    library_filtered['timestamp'] = pd.to_datetime(library_filtered['timestamp'])

    def prepare_df(df, cols):
        return df[cols]

    card_swipes_tl = prepare_df(card_swipes_filtered, ['timestamp', 'event_type', 'location_id'])
    cctv_tl = prepare_df(cctv_filtered, ['timestamp', 'event_type', 'location_id'])
    wifi_tl = prepare_df(wifi_filtered, ['timestamp', 'event_type', 'ap_id'])
    lab_tl = prepare_df(lab_filtered, ['timestamp', 'event_type', 'room_id'])
    notes_tl = prepare_df(notes_filtered, ['timestamp', 'event_type', 'category', 'text'])
    library_tl = prepare_df(library_filtered, ['timestamp', 'event_type', 'book_id'])

    wifi_tl = wifi_tl.rename(columns={'ap_id': 'location'})
    lab_tl = lab_tl.rename(columns={'room_id': 'location'})
    notes_tl = notes_tl.rename(columns={'category': 'location'})
    library_tl = library_tl.rename(columns={'book_id': 'location'})

    all_events = pd.concat([card_swipes_tl, cctv_tl, wifi_tl,
                            lab_tl, notes_tl, library_tl],
                           ignore_index=True, sort=False).sort_values('timestamp')

    if start_date:
        all_events = all_events[all_events['timestamp'] >= pd.to_datetime(start_date)]
    if end_date:
        all_events = all_events[all_events['timestamp'] <= pd.to_datetime(end_date)]
    if event_types:
        all_events = all_events[all_events['event_type'].isin(event_types)]

    all_events = all_events.reset_index(drop=True)

    event_counts = all_events['event_type'].value_counts().to_dict()

    all_events = all_events.sort_values('timestamp')
    all_events['gap'] = all_events['timestamp'].diff().dt.days.fillna(0)
    inactivity_flag = any(all_events['gap'] > 7)

    transition_matrix = build_transition_matrix(all_events)
    last_location = None
    if not all_events.empty:
        last_location = all_events['location'].dropna().iloc[-1]

    predicted_next = predict_next_location(transition_matrix, last_location)

    anomalies = anomaly_detection(all_events)

    return all_events, event_counts, inactivity_flag, predicted_next, anomalies

def export_timeline(timeline, entity_id, file_format='csv'):
    filename = f"timeline_{entity_id}.{file_format}"
    if file_format == 'csv':
        timeline.to_csv(filename, index=False)
    elif file_format == 'json':
        timeline.to_json(filename, orient='records', lines=True)
    else:
        raise ValueError("Unsupported file format. Use 'csv' or 'json'.")
    print(f"Timeline exported to {filename}")

def visualize_timeline(timeline, entity_id):
    if timeline.empty:
        return None
    fig = px.scatter(
        timeline,
        x='timestamp',
        y='event_type',
        color='event_type',
        hover_data=['location', 'text'],
        title=f'Activity Timeline for Entity: {entity_id}',
        labels={'timestamp': 'Timestamp', 'event_type': 'Event Type'},
        height=600
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig
