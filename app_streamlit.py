import streamlit as st
import pandas as pd
from timeline_generator import load_linked_sources, generate_timeline, visualize_timeline

st.set_page_config(page_title="Entity Activity Timeline", layout="wide")
st.title("Entity Activity Timeline")

(card_swipes, cctv, wifi_logs, lab_bookings,
 text_notes, library_checkouts, entity_table, face_embeddings) = load_linked_sources()

with st.form("timeline_form"):
    entity_id = st.text_input("Enter entity_id")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", value=None)
    with col2:
        end_date = st.date_input("End date", value=None)
    event_types_input = st.text_input("Event types (comma-separated, optional)")
    submitted = st.form_submit_button("Generate Timeline")

if submitted:
    if not entity_id:
        st.error("Please enter an entity_id")
    else:
        event_types = [et.strip() for et in event_types_input.split(",")] if event_types_input else None
        try:
            timeline, event_counts, inactivity_flag, predicted_next, anomalies = generate_timeline(
                entity_id, card_swipes, cctv, wifi_logs, lab_bookings,
                text_notes, library_checkouts, entity_table, start_date, end_date, event_types)
        except Exception as e:
            st.exception(f"Error while generating timeline: {e}")
        else:
            st.subheader(f"Timeline for entity: {entity_id}")
            if hasattr(timeline, "shape"):
                st.dataframe(timeline)
            else:
                st.write(timeline)

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

            try:
                csv = timeline.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download timeline as CSV",
                    data=csv,
                    file_name=f"timeline_{entity_id}.csv",
                    mime="text/csv"
                )
            except Exception:
                st.info("Timeline not available for CSV export.")

            try:
                fig = visualize_timeline(timeline, entity_id)
                if fig:
                    st.subheader("Interactive Timeline Visualization")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No events available for visualization.")
            except Exception as e:
                st.info(f"Visualization could not be created: {e}")

st.markdown("---")
st.markdown("**Notes:** This app assumes CSVs are in the repo root. If missing, upload them below.")
