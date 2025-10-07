import streamlit as st
from timeline_generator import (load_linked_sources, cross_source_linking, generate_timeline, visualize_timeline)
from datetime import date
import re
import pandas as pd

def validate_entity_id(eid):
    return bool(re.match(r"^E\d+$", eid))

def main():
    st.title("Entity Activity Timeline Dashboard")

    # Load all data on app start
    card_swipes, cctv, wifi_logs, lab_bookings, text_notes, library_checkouts, entity_table_raw = load_linked_sources()
    linked_data = cross_source_linking()

    profiles = entity_table_raw.copy()
    profiles['student_or_staff_id'] = profiles['student_id'].fillna(profiles['staff_id'])
    entity_table = profiles[['entity_id', 'student_or_staff_id']].drop_duplicates()
    entity_table['entity_id'] = entity_table['entity_id'].astype(str)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        entity_id = st.text_input("Enter Entity ID", help="E.g., E100000")
        start_date = st.date_input("Start date (optional)", value=None)
        end_date = st.date_input("End date (optional)", value=None)

        EVENT_TYPES = ["card_swipe", "cctv_sighting", "wifi_log", "lab_booking", "text_note", "library_checkout"]
        EVENT_TYPES_ALL = ["All"] + EVENT_TYPES
        selected_event_types = st.multiselect("Select Event Types", EVENT_TYPES_ALL, default=["All"])

        generate_btn = st.button("Generate Timeline")

    if generate_btn:
        if not entity_id:
            st.error("Entity ID is required!")
            return
        if not validate_entity_id(entity_id):
            st.error("Invalid Entity ID format. Must start with 'E' followed by digits.")
            return

        sd = start_date.isoformat() if isinstance(start_date, date) else None
        ed = end_date.isoformat() if isinstance(end_date, date) else None
        if "All" in selected_event_types:
            event_types_filter = EVENT_TYPES
        else:
            event_types_filter = selected_event_types

        timeline, event_counts, inactivity_flag, predicted_next, anomalies = generate_timeline(
            entity_id,
            linked_data['card_swipes'], linked_data['cctv_faces'], linked_data['wifi_logs'],
            linked_data['lab_bookings'], linked_data['text_notes'], linked_data['library_checkouts'],
            entity_table, sd, ed, event_types_filter
        )

        if timeline.empty:
            st.info("No events found for the specified filters.")
            return

        st.markdown("---")
        st.subheader("Timeline Table")
        st.dataframe(timeline)

        st.markdown("---")
        st.subheader("Event Counts Summary")
        if event_counts:
            counts_df = pd.DataFrame.from_dict(event_counts, orient='index', columns=['Count']).sort_values('Count', ascending=False)
            st.bar_chart(counts_df)
            with st.expander("See event counts details"):
                st.table(counts_df)
        else:
            st.write("No event counts available.")

        st.markdown("---")
        if inactivity_flag:
            st.warning("⚠️ Inactivity gap detected (>7 days)")

        # Removed Next Predicted Location Section as requested

        st.markdown("---")
        st.subheader(f"Detected Anomalies ({len(anomalies)})")
        if anomalies:
            for anomaly in anomalies:
                st.error(anomaly)
        else:
            st.write("No anomalies detected.")

        st.markdown("---")
        csv = timeline.to_csv(index=False).encode('utf-8')
        st.download_button("Download timeline as CSV", csv, file_name=f"timeline_{entity_id}.csv", mime="text/csv")

        fig = visualize_timeline(timeline, entity_id)
        if fig:
            st.markdown("---")
            st.subheader("Timeline Visualization")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No events available for visualization.")

if __name__ == "__main__":
    main()
