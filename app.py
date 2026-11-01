"""
VERIDEX AI — Streamlit Dashboard Edition
Autonomous Pothole Detection & Contractor Defect Liability Warranty Auditor
Prepared for Techfest IIT Bombay 2026
"""

import os
import time
import math
import tempfile
import cv2
import numpy as np
import pandas as pd
import streamlit as st
import onnxruntime as ort

# --- Page Configuration ---
st.set_page_config(
    page_title="VERIDEX AI — IIT Bombay Techfest",
    page_icon="🕳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
st.markdown("""
<style>
    .main { background-color: #090c10; color: #f0f3f8; }
    .stMetric { background-color: #131822; padding: 12px; border-radius: 10px; border: 1px solid #222c3d; }
    .badge-iitb { background: linear-gradient(135deg, #2563eb, #7c3aed); color: white; padding: 4px 10px; border-radius: 99px; font-weight: 700; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# --- Preloaded Road Database ---
ROADS_DB = [
    {
        "id": "IITB-01",
        "name": "Adi Shankaracharya Marg / JVLR (IIT Bombay Main Gate)",
        "authority": "BMC / MMRDA",
        "contractor": "Larsen & Toubro (L&T Infrastructure)",
        "completed": "2023-10-15",
        "dlp_years": 3,
        "lat": 19.1298, "lng": 72.9150
    },
    {
        "id": "MUM-01",
        "name": "Western Express Highway (WEH) / NH-48",
        "authority": "Maharashtra PWD / MMRDA",
        "contractor": "IRB Infrastructure Developers",
        "completed": "2024-01-20",
        "dlp_years": 5,
        "lat": 19.0800, "lng": 72.8500
    },
    {
        "id": "MUM-02",
        "name": "Eastern Express Highway (EEH)",
        "authority": "BMC / MCGM",
        "contractor": "HCC – Shapoorji Pallonji (JV)",
        "completed": "2022-05-10",
        "dlp_years": 3,
        "lat": 19.0600, "lng": 72.8800
    },
    {
        "id": "NHAI-95",
        "name": "Ludhiana Elevated Highway, NH-95",
        "authority": "NHAI",
        "contractor": "Gammon Engineers – SP Singla (JV)",
        "completed": "2023-09-11",
        "dlp_years": 5,
        "lat": 30.9040, "lng": 75.8500
    }
]

def check_warranty(road_info):
    if not road_info:
        return {"status": "Unknown", "under": None, "msg": "Road not in local contract DB"}
    try:
        from datetime import datetime
        comp_date = datetime.strptime(road_info["completed"], "%Y-%m-%d")
        exp_year = comp_date.year + road_info["dlp_years"]
        exp_date = comp_date.replace(year=exp_year)
        now = datetime.now()
        is_under = now <= exp_date
        return {
            "under": is_under,
            "expiry": exp_date.strftime("%Y-%m-%d"),
            "status": "Under Active DLP Warranty" if is_under else "Warranty Expired",
            "contractor": road_info["contractor"]
        }
    except Exception:
        return {"status": "Unknown", "under": None, "msg": "Date parsing error"}

# --- Load ONNX Model ---
@st.cache_resource
def load_onnx_model(model_path="pothole.onnx"):
    if not os.path.exists(model_path):
        return None
    session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
    return session

session = load_onnx_model()

# --- UI Header ---
col_logo, col_header = st.columns([1, 8])
with col_logo:
    st.markdown("<h1 style='font-size: 55px; margin: 0;'>🕳️</h1>", unsafe_allow_html=True)
with col_header:
    st.markdown("## VERIDEX AI — Road Audit & DLP Warranty Enforcement")
    st.markdown("<span class='badge-iitb'>Techfest IIT Bombay 2026 Showcase</span> &nbsp; Real-time AI Pothole Detection & Photogrammetric Sizing", unsafe_allow_html=True)

st.write("---")

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Configuration & Sensors")

selected_road_name = st.sidebar.selectbox(
    "Monitored Road Corridor",
    options=[r["name"] for r in ROADS_DB]
)
active_road = next((r for r in ROADS_DB if r["name"] == selected_road_name), None)

st.sidebar.markdown("### 📷 Camera Photogrammetry")
cam_height = st.sidebar.slider("Camera Height above Road (m)", 0.5, 3.5, 1.2, 0.05)
cam_tilt = st.sidebar.slider("Tilt Angle Down (°)", 0.0, 45.0, 10.0, 0.5)
cam_fov = st.sidebar.slider("Lens Field of View (°)", 40, 110, 70, 1)

st.sidebar.markdown("### 🎯 Detection Sensitivity")
conf_threshold = st.sidebar.slider("Confidence Threshold", 0.20, 0.90, 0.45, 0.05)

st.sidebar.write("---")
video_source = st.sidebar.radio(
    "Video Stream Source",
    options=["Sample Dashcam Video (IITB Venue)", "Upload Custom Video"]
)

uploaded_file = None
if video_source == "Upload Custom Video":
    uploaded_file = st.sidebar.file_uploader("Upload MP4 / MOV Video", type=["mp4", "mov", "avi"])

# --- Main Layout ---
if not session:
    st.error("⚠️ `pothole.onnx` model file not found in current folder. Download or train the model to begin.")
    st.stop()

# Video playback & Inference
video_path = "sample-road-video.mp4"
if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    video_path = tfile.name

col_stream, col_telemetry = st.columns([1.4, 1])

with col_stream:
    st.markdown("#### 📹 Real-Time Dashcam Stream & Photogrammetric HUD")
    video_placeholder = st.empty()
    status_placeholder = st.empty()

with col_telemetry:
    st.markdown("#### 📊 Fleet Telemetry & Contractor Liability")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1_metric = kpi1.empty()
    kpi2_metric = kpi2.empty()
    kpi3_metric = kpi3.empty()

    warranty_info = check_warranty(active_road)
    st.markdown(f"""
    **Assigned Authority:** `{active_road['authority']}`  
    **Contractor on Record:** `{active_road['contractor']}`  
    **Defect Liability Status:** **`{warranty_info['status']}`**  
    """)

    st.markdown("#### 🗺️ Venue GPS Coordinate Fix")
    map_placeholder = st.empty()

# Start Process Button
if st.button("▶️ Start Autonomous Road Audit", type="primary"):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        st.error("Error opening video file.")
        st.stop()

    total_potholes = 0
    severe_count = 0
    detected_records = []
    focal_px = (640 / 2) / math.tan(cam_fov * math.pi / 360)
    theta_rad = cam_tilt * math.pi / 180

    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1

        # Resize for YOLO
        h_orig, w_orig = frame.shape[:2]
        blob = cv2.resize(frame, (640, 640))
        img_input = blob[:, :, ::-1].transpose(2, 0, 1).astype(np.float32) / 255.0
        img_input = np.expand_dims(img_input, 0)

        # Run inference
        outputs = session.run(None, {'images': img_input})
        out0 = outputs[0]  # [1, 37, 8400] or [1, 5, 8400]

        # Extract detections for class 0 (pothole)
        confs = out0[0, 4, :]
        valid_indices = np.where(confs >= conf_threshold)[0]

        frame_annotated = frame.copy()
        current_frame_dets = 0

        for idx in valid_indices:
            conf = float(confs[idx])
            cx, cy, w, h = out0[0, :4, idx]

            # Scale to original resolution
            scale_x = w_orig / 640.0
            scale_y = h_orig / 640.0
            x1 = int((cx - w / 2) * scale_x)
            y1 = int((cy - h / 2) * scale_y)
            x2 = int((cx + w / 2) * scale_x)
            y2 = int((cy + h / 2) * scale_y)

            # Ground plane distance calculation
            v = y2 * (640.0 / h_orig)
            u = ((x1 + x2) / 2) * (640.0 / w_orig)
            y_norm = (v - 320) / focal_px
            den = math.sin(theta_rad) + y_norm * math.cos(theta_rad)

            fwd_m = 5.0
            width_m = 0.45
            if den > 1e-4:
                t = cam_height / den
                fwd_m = max(1.0, min(30.0, t * (math.cos(theta_rad) - y_norm * math.sin(theta_rad))))
                width_m = (w / 640.0 * w_orig) * t / focal_px

            sev = "High" if width_m > 0.60 else ("Medium" if width_m > 0.30 else "Low")
            color = (0, 0, 255) if sev == "High" else ((0, 165, 255) if sev == "Medium" else (0, 255, 0))

            # Draw box & HUD
            cv2.rectangle(frame_annotated, (x1, y1), (x2, y2), color, 3)
            label = f"POTHOLE ({sev}) ~{width_m:.2f}m ({int(conf*100)}%)"
            cv2.putText(frame_annotated, label, (x1, max(20, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)

            current_frame_dets += 1
            if current_frame_dets == 1 and frame_idx % 8 == 0:
                total_potholes += 1
                if sev == "High":
                    severe_count += 1
                detected_records.append({
                    "ID": f"PH-{frame_idx:04d}",
                    "Severity": sev,
                    "Width (m)": round(width_m, 2),
                    "Distance (m)": round(fwd_m, 1),
                    "Confidence": f"{int(conf*100)}%",
                    "Road": active_road["name"],
                    "Contractor": active_road["contractor"],
                    "DLP Liability": "Contractor Liable" if warranty_info.get("under") else "PWD Maintenance"
                })

        # Update video display
        frame_rgb = cv2.cvtColor(frame_annotated, cv2.COLOR_BGR2RGB)
        video_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

        # Update telemetry
        kpi1_metric.metric("Total Potholes", total_potholes)
        kpi2_metric.metric("Severe (>60cm)", severe_count)
        kpi3_metric.metric("Under DLP", total_potholes if warranty_info.get("under") else 0)

        time.sleep(0.03)

    cap.release()
    status_placeholder.success("Road audit run completed successfully!")

    # Display Results Register
    if detected_records:
        st.write("---")
        st.markdown("### 📋 Official Road Defect & Warranty Audit Register")
        df = pd.DataFrame(detected_records)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Official Audit CSV Report",
            data=csv,
            file_name="VERIDEX_Techfest_Road_Audit.csv",
            mime="text/csv"
        )
