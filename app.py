import streamlit as st
from timeline_generator import (load_linked_sources, generate_timeline,
                                export_timeline, visualize_timeline)

def main():
    st.title("Entity Activity Timeline")

    (card_swipes, cctv, wifi_logs, lab_bookings,
     text_notes, library_checkouts, entity_table) = load_linked_sources()

    entity_id = st.text_input("Enter entity_id")
    start_date = st.date_input("Start date", value=None)
    end_date = st.date_input("End date", value=None)
    event_types_input = st.text_input("Event types (comma-separated, optional)")

    if st.button("Generate Timeline"):
        if not entity_id:
            st.error("Please enter an entity_id")
            return

        event_types = [et.strip() for et in event_types_input.split(",")] if event_types_input else None

        timeline, event_counts, inactivity_flag, predicted_next, anomalies = generate_timeline(
            entity_id, card_swipes, cctv, wifi_logs, lab_bookings,
            text_notes, library_checkouts, entity_table,
            start_date, end_date, event_types)

        st.subheader(f"Timeline for entity: {entity_id}")
        st.dataframe(timeline)

        st.subheader("Event Counts")
        st.write(event_counts)

        if inactivity_flag:
            st.warning("Inactivity gap detected (>7 days)")

        st.subheader("Next Predicted Location")
        if predicted_next:
            st.success(f"Next likely location: {predicted_next}")
        else:
            st.info("Insufficient data for prediction.")

        st.subheader("Detected Anomalies")
        if anomalies:
            for anomaly in anomalies:
                st.error(anomaly)
        else:
            st.info("No anomalies detected in timeline.")

        csv = timeline.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download timeline as CSV",
            data=csv,
            file_name=f"timeline_{entity_id}.csv",
            mime='text/csv'
        )

        fig = visualize_timeline(timeline, entity_id)
        if fig:
            st.subheader("Interactive Timeline Visualization")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No events available for visualization.")

if __name__ == "__main__":
    main()
