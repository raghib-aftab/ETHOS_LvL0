# 🏫 Campus Entity Resolution & Security Monitoring System
*A Cross-Source Analytics Platform for Campus Activity Intelligence*

## 🔍 Overview
Modern campuses generate enormous amounts of operational data — from Wi-Fi logs and card swipes to CCTV frames, library checkouts, lab bookings, and free-text notes.  
However, these datasets often remain siloed, making it difficult for administrators and security teams to monitor activities, ensure safety, or detect anomalies.

This project presents an **Entity Resolution & Security Monitoring Platform** that unifies multi-source campus data into a single explainable system — reconstructing entity timelines, predicting activity gaps, and surfacing anomalies through a clean, interactive dashboard.

Developed as part of **Saptang Labs – Ethos Hack 2025 (Product Development Track)**, this system demonstrates a deployable solution that bridges data engineering, analytics, and security intelligence.

---

## 🎯 Objectives
The system addresses the core objectives of the challenge:

| Module | Description |
|---------|--------------|
| **Entity Resolution** | Resolve student/staff/asset identities across heterogeneous data sources using card IDs, device hashes, or facial embeddings. |
| **Cross-Source Linking** | Join structured data (swipes, Wi-Fi, bookings, notes, etc.) into a unified entity representation. |
| **Timeline Generation** | Build chronological activity histories for any entity and visualize them interactively. |
| **Predictive Monitoring** | Estimate the most likely next location based on learned transition probabilities. |
| **Anomaly Detection** | Flag inactivity gaps, unseen locations, or abnormal activity counts. |
| **Security Dashboard (UI)** | Intuitive Streamlit interface for exploration, query, and timeline visualization. |

---

## 🧠 System Architecture
**Core Components:**

1. **Data Ingestion (`load_data.py`)** — Loads structured campus datasets directly from the root directory using `pandas`.  
2. **Entity Resolution (`entity_resolution.py`)** — Consolidates student and staff identifiers into a unified entity table, mapping all keys (card_id, device_hash, face_id).  
3. **Cross-Source Linking (`cross_source_linking.py`)** — Performs joins between entity table and domain-specific logs — ensuring every data point traces back to a unique entity.  
4. **Timeline Generator (`timeline_generator.py`)** — Integrates all activity sources, reconstructs entity timelines, detects anomalies, and predicts next probable location.  
5. **Streamlit Application (`app.py`)** — Provides an interactive UI for querying entities, visualizing activity timelines, exporting data, and exploring anomalies.

---

## ⚙️ Tech Stack
- **Language:** Python 3.10+  
- **Framework:** Streamlit  
- **Libraries:** Pandas, Plotly, Collections, OS  

---

## 📂 Repository Structure
```
│
├── app.py                      # Streamlit interface for the entire system
├── timeline_generator.py        # Core logic for timeline, anomaly detection & prediction
├── cross_source_linking.py      # Multi-source data linking
├── entity_resolution.py         # Unification of entity identities
├── load_data.py                 # Data ingestion & validation
├── requirements.txt             # Dependencies
│
├── campus_card_swipes.csv
├── cctv_frames.csv
├── face_embeddings.csv
├── free_text_notes.csv
├── lab_bookings.csv
├── library_checkouts.csv
├── student-or-staff-profiles.csv
└── wifi_associations_logs.csv
```

---

## 🚀 Deployment
### 🔧 Local Setup
```bash
# Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### ☁️ Streamlit Cloud
Simply upload this repository to Streamlit Cloud.  
The flat directory structure ensures seamless deployment — no `src/` or `data/` folders required.

---

## 📊 Features Showcase
- **Interactive Timeline Visualization:** Explore entity activities with Plotly scatter plots.  
- **Anomaly Detection:** Automatically highlights inactivity gaps, unseen locations, and unusual event counts.  
- **Predictive Insights:** Estimates the next likely location of a person or device based on recent movement history.  
- **Data Export:** Download generated timelines as CSVs directly from the UI.

---

## 🧩 Evaluation Mapping
| Challenge Criterion | Implementation |
|----------------------|----------------|
| **Entity Resolution Accuracy (25%)** | Unified entity table mapping `entity_id`, `card_id`, `device_hash`, and `face_id`. |
| **Cross-Source Linking (25%)** | Consistent joining of all structured datasets via shared keys. |
| **Timeline Generation (20%)** | Complete event stream aggregation and visualization per entity. |
| **Predictive Monitoring (15%)** | Transition matrix–based location prediction. |
| **Security Dashboard (10%)** | User-friendly Streamlit UI for timeline and anomaly visualization. |
| **Robustness & Privacy (5%)** | Handles missing identifiers and supports explainable insights without personal data exposure. |

---

## 🔐 Privacy & Ethical Use
The datasets are **synthetic and anonymized**.  
All processing and visualization components are built for research, security analytics, and system evaluation purposes only.

---

## 🏁 Conclusion
This project demonstrates a **deployable, modular, and privacy-aware campus monitoring system** — seamlessly integrating data fusion, anomaly detection, and explainable prediction through an accessible dashboard.

It reflects the **Product Development Track** goals of *Ethos Hack 2025 by Saptang Labs*:  
> “Design a system that bridges campus data silos into actionable, explainable intelligence.”

---

## 👥 Contributors
- **Raghib Aftab** – System Design, Data Fusion, Visualization  
- (Add any teammates or mentors here)

---

## 🧾 License
This project is released under the **MIT License**.
