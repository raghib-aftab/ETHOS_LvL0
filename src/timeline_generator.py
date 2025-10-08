import pandas as pd
from collections import defaultdict
from tabulate import tabulate
from load_data import load_linked_sources
from cross_source_linking import cross_source_linking
import plotly.express as px

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
    next_locs = transition_matrix[current_location]
    return max(next_locs, key=next_locs.get)

def anomaly_detection(timeline):
    anomalies = []
    # Detect inactivity gaps > 14 days
    gaps = timeline['timestamp'].diff().dt.days.fillna(0)
    large_gaps = timeline[gaps > 14]
    for idx, row in large_gaps.iterrows():
        anomalies.append(f"Inactivity gap of {int(gaps.iloc[idx])} days before {row['timestamp'].date()}")

    # Define allowed locations (lab rooms) to exclude from location anomaly detection
    allowed_locations = set(timeline[timeline['event_type'] == 'lab_booking']['location'].dropna().unique())

    seen_locations = set()
    for idx, loc in enumerate(timeline['location']):
        if pd.isna(loc):
            continue
        # Skip allowed lab locations
        if loc in allowed_locations:
            continue
        if loc not in seen_locations and len(seen_locations) > 0:
            anomalies.append(f"Unexpected visit to location '{loc}' at {timeline.loc[idx, 'timestamp']}")
        seen_locations.add(loc)

    # Abnormal spikes in daily event counts
    timeline['date'] = timeline['timestamp'].dt.date
    daily_counts = timeline.groupby('date').size()
    mean = daily_counts.mean() if len(daily_counts) > 1 else 0
    std = daily_counts.std() if len(daily_counts) > 1 else 0
    for date, count in daily_counts.items():
        if std != 0 and abs(count - mean) > 2 * std:
            anomalies.append(f"Unusual activity level ({count} events) on {date}")

    # Remove duplicates preserving order
    seen = set()
    unique_anomalies = []
    for a in anomalies:
        if a not in seen:
            seen.add(a)
            unique_anomalies.append(a)

    return unique_anomalies

def generate_timeline(entity_id, card_swipes, cctv_faces, wifi_logs, lab_bookings,
                      text_notes, library_checkouts, entity_table,
                      start_date=None, end_date=None, event_types=None):
    def filter_and_prepare(df, filter_col='entity_id', time_col='timestamp', event_name='event'):
        filtered = df[df[filter_col] == entity_id].copy()
        filtered[time_col] = pd.to_datetime(filtered[time_col])
        filtered['event_type'] = event_name
        filtered['entity_id'] = entity_id
        return filtered

    card_filtered = filter_and_prepare(card_swipes, 'entity_id', 'timestamp', 'card_swipe')
    cctv_filtered = filter_and_prepare(cctv_faces, 'entity_id', 'timestamp', 'cctv_sighting')
    wifi_filtered = filter_and_prepare(wifi_logs, 'entity_id', 'timestamp', 'wifi_log')
    lab_filtered = filter_and_prepare(lab_bookings, 'entity_id', 'start_time', 'lab_booking')
    notes_filtered = filter_and_prepare(text_notes, 'entity_id', 'timestamp', 'text_note')
    library_filtered = filter_and_prepare(library_checkouts, 'entity_id', 'timestamp', 'library_checkout')

    def prepare_df(df, cols):
        for col in cols:
            if col not in df.columns:
                df[col] = None
        return df[cols]

    card_tl = prepare_df(card_filtered, ['timestamp', 'event_type', 'location_id', 'entity_id']).rename(columns={'location_id':'location'})
    cctv_tl = prepare_df(cctv_filtered, ['timestamp', 'event_type', 'location_id', 'entity_id']).rename(columns={'location_id':'location'})
    wifi_tl = prepare_df(wifi_filtered, ['timestamp', 'event_type', 'ap_id', 'entity_id']).rename(columns={'ap_id':'location'})
    lab_tl = prepare_df(lab_filtered, ['start_time', 'event_type', 'room_id', 'entity_id']).rename(columns={'start_time':'timestamp','room_id':'location'})
    notes_tl = prepare_df(notes_filtered, ['timestamp', 'event_type', 'category', 'text', 'entity_id']).rename(columns={'category':'location'})
    library_tl = prepare_df(library_filtered, ['timestamp', 'event_type', 'book_id', 'entity_id']).rename(columns={'book_id':'location'})

    all_events = pd.concat([card_tl, cctv_tl, wifi_tl, lab_tl, notes_tl, library_tl], ignore_index=True).sort_values('timestamp')

    if start_date:
        all_events = all_events[all_events['timestamp'] >= pd.to_datetime(start_date)]
    if end_date:
        all_events = all_events[all_events['timestamp'] <= pd.to_datetime(end_date)]
    if event_types:
        all_events = all_events[all_events['event_type'].isin(event_types)]

    all_events.reset_index(drop=True, inplace=True)

    event_counts = all_events['event_type'].value_counts().to_dict()
    all_events['gap'] = all_events['timestamp'].diff().dt.days.fillna(0)
    inactivity_flag = any(all_events['gap'] > 7)

    transition_matrix = build_transition_matrix(all_events)
    last_location = all_events['location'].dropna().iloc[-1] if not all_events.empty else None
    predicted_next = predict_next_location(transition_matrix, last_location)
    anomalies = anomaly_detection(all_events)

    entity_info = entity_table[['entity_id', 'student_or_staff_id']].drop_duplicates()
    all_events = pd.merge(all_events, entity_info, on='entity_id', how='left')
    all_events = all_events.drop(columns=['entity_id'])

    return all_events, event_counts, inactivity_flag, predicted_next, anomalies

def visualize_timeline(timeline, entity_id):
    if timeline.empty:
        return None
    fig = px.scatter(
        timeline.sort_values('timestamp'),
        x='timestamp',
        y='event_type',
        color='event_type',
        hover_data=['location', 'text', 'student_or_staff_id'],
        title=f"Activity Timeline for Entity: {entity_id}",
        labels={'timestamp': 'Timestamp', 'event_type': 'Event Type'},
        height=600
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

def print_full_timeline(timeline_df, entity_id):
    print(f"\n{'='*70}\nTimeline of Entity: {entity_id}\n{'='*70}")
    print(tabulate(timeline_df, headers='keys', tablefmt='fancy_grid', showindex=False))

def print_summary(timeline_df, event_counts, inactivity_flag, predicted_next, anomalies):
    print("\n" + "="*70)
    print(f"{'TIMELINE SUMMARY':^70}")
    print("="*70)
    print(f"Total Events: {len(timeline_df)}")
    print("\nEvent counts:")
    for etype, count in sorted(event_counts.items()):
        print(f"  - {etype:<20} : {count}")
    print(f"\nInactivity Gaps (> 7 days): {'YES' if inactivity_flag else 'NO'}")
    if not timeline_df.empty:
        print(f"\nLast known location: {timeline_df['location'].dropna().iloc[-1]}")
        print(f"Last event timestamp: {timeline_df['timestamp'].iloc[-1]}")
    else:
        print("No timeline data available.")
    print(f"\nPredicted next location: {predicted_next if predicted_next else 'N/A'}")
    print(f"\nDetected anomalies ({len(anomalies)}):")
    for i, a in enumerate(anomalies[:5], 1):
        print(f"  {i}. {a}")
    print("="*70)

def main():
    entity_id = input("Enter Entity ID (e.g., E100000): ").strip()
    start_date = input("Start date (YYYY-MM-DD) or Enter to skip: ").strip() or None
    end_date = input("End date (YYYY-MM-DD) or Enter to skip: ").strip() or None
    event_types_in = input("Event types comma-separated or Enter for all: ").strip()
    event_types = [et.strip() for et in event_types_in.split(',')] if event_types_in else None

    linked_data = cross_source_linking()
    _, _, _, _, _, _, profiles = load_linked_sources()
    profiles['student_or_staff_id'] = profiles['student_id'].fillna(profiles['staff_id'])
    entity_table = profiles[['entity_id', 'student_or_staff_id']].drop_duplicates()
    entity_table['entity_id'] = entity_table['entity_id'].astype(str)

    timeline, event_counts, inactivity_flag, predicted_next, anomalies = generate_timeline(
        entity_id, linked_data['card_swipes'], linked_data['cctv_faces'],
        linked_data['wifi_logs'], linked_data['lab_bookings'], linked_data['text_notes'],
        linked_data['library_checkouts'], entity_table, start_date, end_date, event_types
    )

    print_full_timeline(timeline, entity_id)
    print_summary(timeline, event_counts, inactivity_flag, predicted_next, anomalies)

if __name__ == "__main__":
    main()
