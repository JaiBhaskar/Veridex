<div align="center">

# 🕳️ VERIDEX AI
### *Autonomous Road Defect Detection & Contractor Warranty Enforcement Engine*

**Real-time Edge Computer Vision · Monocular 3D Photogrammetry · Legal DLP Warranty Enforcement**

<br>

[![Live Vercel Deployment](https://img.shields.io/badge/🚀_LIVE_DEMO-veridex--omega.vercel.app-00DC82?style=for-the-badge&logo=vercel&logoColor=white)](https://veridex-omega.vercel.app)
[![GitHub Repository](https://img.shields.io/badge/GitHub-JaiBhaskar%2FVeridex-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/JaiBhaskar/Veridex)
[![Architecture: YOLOv8](https://img.shields.io/badge/Vision_AI-YOLOv8_ONNX-FF5722?style=for-the-badge)](https://onnxruntime.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](#)

<br>

> 🌐 **Experience the Live Web App in your browser:**  
> 👉 **[https://veridex-omega.vercel.app](https://veridex-omega.vercel.app)** 👈  
> *(Zero installation required · Works instantly on iPhone, Android, and Desktop with Camera & GPS)*

</div>

---

## 💡 The Core Problem & Innovation

| The Traditional Blame Game ❌ | The VERIDEX Solution 🟢 |
| :--- | :--- |
| **Citizens complain** about potholes, but municipalities and contractors pass the blame. | **Instant legal accountability:** Matches GPS coordinates with public infrastructure contracts in real time. |
| **Expensive specialized survey vehicles** (₹50+ Lakhs) with LiDAR required to scan roads. | **Runs on any regular smartphone or dashcam:** 100% on-device AI with zero cloud server costs. |
| **Public pays repeatedly:** Municipalities spend citizen taxes patching roads that are already under warranty. | **Automated warranty enforcement:** Flags private contractors liable under 3–5 year **Defect Liability Period (DLP)** clauses to repair defects for free. |

---

## ✨ Key Features

```
  📷 Live Dashcam / Phone Camera
               │
               ▼
  🧠 Edge AI Inference (30+ FPS)  ──────────►  Runs 100% on device via WebAssembly SIMD
               │
               ▼
  📐 3D Photogrammetry Sizing   ────────────►  Measures metric pothole width in centimeters
               │
               ▼
  🛰️ Pan-India Live Road Geocoder ──────────►  Identifies highway, district, and NHAI/PWD authority
               │
               ▼
  ⚖️ DLP Warranty Audit Engine   ──────────►  Checks contractor liability & calculates repair costs
               │
               ▼
  📊 Actionable Output          ────────────►  Instant Legal Notice, Leaflet Map Pin & CSV Report
```

- ⚡ **Real-Time Edge Computer Vision:** Custom YOLOv8 neural network runs directly inside the client browser at **30+ FPS** via ONNX Runtime Web.
- 📏 **No LiDAR Needed (Photogrammetric 3D Sizing):** Automatically calculates pothole forward distance (m), lateral lane offset (m), and physical metric width (cm).
- 🗺️ **Pan-India Road Intelligence:** Queries live OpenStreetMap reverse-geocoding to detect any highway, expressway, or city road in India.
- 🏛️ **Government DLP Warranty Auditor:** Automatically cross-references contractor warranty clauses (**5-Year NHAI EPC** / **3-Year State PWD** / **2-Year Urban Municipal**).
- 📍 **Interactive Esri Street Map:** High-precision defect pins with live popup telemetry and GPS coordinates.
- 📱 **Mobile-First Responsive UI:** Designed with thumb-friendly controls, camera flip support, and native defect audit cards for smartphones.
- 📥 **Executive Excel CSV Report:** Generates UTF-8 encoded audit sheets with formatted dates, repair liabilities in ₹ INR, and clickable Google Maps links.

---

## 📐 How 3D Photogrammetry Works (Without Expensive LiDAR)

VERIDEX uses **single-camera flat-road trigonometry** to calculate the real metric dimensions of potholes directly from 2D pixels:

```
                   Camera Mount (h = 1.2m)
                        ▲
                        │ \
                        │   \  Optical Ray to Bottom of Pothole
     Optical Center ────┼─────\────────────────────── Horizon Line
                        │       \  θ (Pitch Tilt Angle: 10°)
                        │         \
════════════════════════╧═══════════\═══════════════════════ Flat Road Plane
                        |<── d (Forward Distance) ──>|
```

### The 3-Step Math (Simplified):
1. **Focal Length ($f$):** Derived from the camera's optical field of view:
   $$f = \frac{\text{Image Width} / 2}{\tan(\text{FOV} / 2)}$$
2. **Ground Projection ($d$):** Traces the bottom edge of the bounding box to the road plane using camera mount height ($h$) and downward tilt angle ($\theta$).
3. **Physical Metric Width ($w$):** Computes the actual physical width in centimeters:
   $$w_{\text{metric}} = \frac{\text{Pixel Width} \times \text{Distance}}{f}$$

### Defect Severity & Liability Cost Matrix:
| Severity Badge | Measured Width | Category | Estimated Repair Cost |
| :---: | :---: | :---: | :---: |
| 🟢 **Low** | $< 30\text{ cm}$ | Surface Depressions & Cracks | **₹1,500** |
| 🟡 **Medium** | $30\text{ cm} - 60\text{ cm}$ | Standard Road Pothole | **₹4,500** |
| 🔴 **High / Severe** | $> 60\text{ cm}$ | Hazardous Road Crater | **₹9,500** |

---

## 🌐 Live Production Demo

### 👉 [https://veridex-omega.vercel.app](https://veridex-omega.vercel.app)

> [!TIP]
> **Mobile Phone Testing:** Open the URL in mobile Chrome or Safari. Tap **"Use Camera"** to turn your phone into an active road audit scanner!

---

## 🛠️ Step-by-Step Setup & How to Run

### Method 1: Instant Browser Run (No Installation)
Visit **[https://veridex-omega.vercel.app](https://veridex-omega.vercel.app)** on any device. Everything (AI model, map, and sample footage) downloads and runs in memory offline.

---

### Method 2: Run Locally on Laptop

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/JaiBhaskar/Veridex.git
   cd Veridex
   ```

2. **Start the Multi-Threaded Local Server:**
   ```bash
   python serve.py
   ```

3. **Open in Browser:**
   * **URL:** `http://localhost:8000` (or `http://127.0.0.1:8000`)

---

### Method 3: Desktop Python Analytics Dashboard (Streamlit)
For presentation slides and offline batch analytics:

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

---

### Method 4: Deploy Your Own Copy to Vercel
```bash
npx vercel --prod --yes
```

---

## 🎮 How to Use the App (User Walkthrough)

```
[ Step 1: Video Input ]   ──►  Tap "📷 Use Camera" or "🚗 Play Sample Video"
                                      │
[ Step 2: AI Detection ]  ──►  Tap "▶ Start Detecting" (Neon AI boxes appear live)
                                      │
[ Step 3: Map Inspection] ──►  Inspect real-time defect pins on the Esri Street Map
                                      │
[ Step 4: Booth Demo ]    ──►  Tap "⚡ Test Pothole" to simulate an instant detection
                                      │
[ Step 5: Enforcement ]   ──►  Tap "📋 Copy Notice" or "📥 Export CSV" for Excel report
```

### What the "⚡ Test Pothole" Button Does:
Designed specifically for **indoor hackathons, presentations, and judge demos**:
* Captures the current camera/stage view.
* Simulates an immediate 94% confidence road defect.
* Triggers the audio feedback alert chime.
* Drops a pin onto the live map.
* Adds an entry to the audit register with contractor DLP status and ₹ liability.
* Generates an official, copyable government legal repair notice!

---

## 📁 Repository Structure

```
├── index.html              # Main Production Edge Web App (YOLOv8, Esri Map, Mobile UI)
├── pothole.onnx            # Trained YOLOv8 Neural Network Weights (13.28 MB)
├── sample-road-video.mp4   # 1080p Real-World Highway Test Dashcam Video
├── serve.py                # Multi-Threaded Dual-Stack Local Server (IPv4 + IPv6)
├── app.py                  # Streamlit Companion Analytics Dashboard
├── vercel.json             # Vercel Production Static Edge Configuration
├── .vercelignore           # Vercel Deployment Optimization Rules
├── manifest.json           # Progressive Web App (PWA) Manifest
├── requirements.txt        # Python Dependencies (Streamlit, ONNX Runtime, OpenCV)
└── README.md               # Project Documentation & Architecture Guide
```

---

<div align="center">

**VERIDEX AI** — *Empowering Citizen Audits & Transparent Public Road Infrastructure.*

Made for **Techfest IIT Bombay** · [Live App](https://veridex-omega.vercel.app) · [GitHub Repo](https://github.com/JaiBhaskar/Veridex)

</div>
