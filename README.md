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

**Language:** Python 3.10+  
**Framework:** Streamlit (for interactive web-based UI)  

### 🧩 Core Libraries  
- **Pandas** – Data processing, cleaning, and multi-source integration  
- **Plotly** – Interactive timeline visualizations and charts  
- **Collections** – Data structures like `defaultdict` for transition tracking  
- **OS** – File and directory path management  
- **Tabulate** – Neat table formatting during debugging  

### 💾 Data Handling & Export  
- **Openpyxl** – Excel file support  
- **Python-docx** – Word report generation  
- **fpdf** – PDF export support  

### 🌐 Deployment & Environment  
- **Streamlit Cloud / Localhost** – One-click deployment  
- **GitHub** – Version control and project hosting  
- **requirements.txt** – Dependency management  

### 📤 Download Feature  
Implemented via **Streamlit’s `st.download_button()`** to export timelines as downloadable CSVs directly from the app.  

---

## 📂 Repository Structure  

```
│
├── src/
│   ├── app.py
│   ├── timeline_generator.py
│   ├── cross_source_linking.py
│   ├── entity_resolution.py
│   └── load_data.py
│
├── data/
│   ├── campus_card_swipes.csv
│   ├── cctv_frames.csv
│   ├── face_embeddings.csv
│   ├── free_text_notes.csv
│   ├── lab_bookings.csv
│   ├── library_checkouts.csv
│   ├── student-or-staff-profiles.csv
│   └── wifi_associations_logs.csv
│
├── requirements.txt
└── README.md
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

---

## 📊 Features Showcase  
- **Interactive Timeline Visualization:** Explore entity activities with Plotly scatter plots.  
- **Anomaly Detection:** Automatically highlights inactivity gaps, unseen locations, and unusual event counts.  
- **Predictive Insights:** Estimates the next likely location of a person or device based on recent movement history.  
- **Data Export:** Download generated timelines as CSVs directly from the UI.  

---

## 🔐 Privacy & Ethical Use  
The datasets are **synthetic and anonymized**.  
All processing and visualization components are built for research, security analytics, and system evaluation purposes only.  

---

## 🏁 Conclusion  
This project demonstrates a **deployable, modular, and privacy-aware campus monitoring system** — seamlessly integrating data fusion, anomaly detection, and explainable prediction through an accessible dashboard.  

---

## 👥 Contributors  
- **Vaibhav Gupta** – Cross-source linking, Timeline generation and Analytics.  
- **Roshan Kumar Sahu** – Data loading and Preparation.  
- **Raghib Aftab** – Streamlit UI and Integration.  
- **Husendra Kumar** – Entity resolution.  
