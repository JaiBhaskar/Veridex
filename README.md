# 🕳️ VERIDEX — Real-Time Road Defect Detection & Contractor Warranty Enforcement

> Autonomous edge computer vision, photogrammetric 3D pothole measurement, and legal Defect Liability Period (DLP) warranty enforcement for Indian roads and highways.

[![Live Web App](https://img.shields.io/badge/Live_App-veridex--omega.vercel.app-000?style=for-the-badge&logo=vercel)](https://veridex-omega.vercel.app)
[![GitHub Repository](https://img.shields.io/badge/GitHub-JaiBhaskar%2FVeridex-181717?style=for-the-badge&logo=github)](https://github.com/JaiBhaskar/Veridex)
[![AI Engine](https://img.shields.io/badge/Model-YOLOv8_ONNX_Web-FF5722?style=for-the-badge)](https://onnxruntime.ai)

---

## 📌 Project Overview

In India, road craters and potholes cause thousands of fatal accidents and millions of rupees in vehicular damage every year. While raw computer vision detection exists, traditional systems fail to solve the accountability bottleneck:
> **"Who constructed this road, who is legally obligated to repair it, and who bears the financial liability?"**

Under Indian infrastructure standards (**NHAI, MoRTH, State PWD, and Smart City Mission EPC/HAM contracts**), newly constructed and resurfaced roads carry a mandatory **Defect Liability Period (DLP / Warranty)** typically lasting **3 to 5 years**. During active DLP:
1. The **contractor is legally required** to repair any road defect within **48–72 hours** at zero expense to the public.
2. If the DLP warranty has expired, financial responsibility shifts to the government municipal/PWD maintenance budget.

**VERIDEX** solves this end-to-end. Running entirely on edge devices (smartphones, dashcams, or tablets) with **zero cloud inference costs**, it detects road defects in real time, computes their real-world metric dimensions (centimeters and meters) via flat-road photogrammetry, resolves the governing authority and contractor in real time across India, and issues legal DLP warranty notices with clickable GPS links.

---

## ⚙️ Technical Architecture

```
[ Video Feed (Camera / Dashcam) ]
               │
               ▼
   [ Letterbox Pre-processing (640x640) ]
               │
               ▼
   [ Edge Neural Network: YOLOv8 ]  ◄── ONNX Runtime Web (WASM SIMD)
               │
               ▼
   [ Bounding Box & Class Decoding ]
               │
               ▼
   [ Multi-Frame Spatial Tracker ]
               │
      ┌────────┴──────────────────────────┐
      ▼                                   ▼
[ Photogrammetric 3D Sizing ]     [ Pan-India Geocoding & Jurisdiction ]
- Metric Width (cm)               - OpenStreetMap Nominatim API
- Forward Distance (m)            - NHAI / State PWD / Urban ULB
- Lateral Lane Offset (m)         - DLP Clause & Contractor Match
      │                                   │
      └────────┬──────────────────────────┘
               ▼
   [ Real-Time Executive HUD & Audit Pipeline ]
   - Neon ADAS Bounding Boxes
   - Esri World Street Map Defect Pin
   - Financial Repair Liability Calculator (₹)
   - Official Legal Notice Generator
   - UTF-8 Executive CSV Audit Exporter
```

### 1. Neural Network Inference Engine
* **Model Architecture:** YOLOv8 edge detector (`pothole.onnx`, 13.2 MB).
* **Runtime:** ONNX Runtime Web 1.18 running locally inside the browser via WebAssembly (WASM).
* **Input Resolution:** `[1, 3, 640, 640]` normalized RGB.
* **Latency:** ~25–35 ms per frame on standard smartphone hardware (30+ FPS).
* **Data Privacy:** 100% on-device processing. No video frames are ever transmitted to third-party servers.

### 2. Monocular Photogrammetry Formulation
VERIDEX computes metric dimensions directly from single-camera 2D pixels without requiring expensive LiDAR sensors:

* **Camera Focal Length from Field of View:**
  $$f = \frac{W / 2}{\tan\left(\frac{\theta_{\text{FOV}}}{2}\right)}$$

* **Ground-Plane Ray Intersection:**
  For bounding box bottom-center $(u, v)$ with image optical center $(c_x, c_y) = (W/2, H/2)$:
  $$y_{\text{norm}} = \frac{v - c_y}{f}, \quad x_{\text{norm}} = \frac{u - c_x}{f}$$
  $$\text{Denominator} = \sin(\theta_{\text{pitch}}) + y_{\text{norm}} \cos(\theta_{\text{pitch}})$$
  $$\text{Optical Depth } t = \frac{h_{\text{mount}}}{\text{Denominator}}$$
  $$\text{Forward Distance } d = t \cdot \left(\cos(\theta_{\text{pitch}}) - y_{\text{norm}} \sin(\theta_{\text{pitch}})\right)$$
  $$\text{Lateral Offset } x = t \cdot x_{\text{norm}}$$

* **Metric Defect Width:**
  $$w_{\text{metric}} = \frac{(x_2 - x_1) \cdot t}{f} \quad (\text{meters})$$

* **Defect Severity Classification:**
  * **Low:** Width $< 30\text{ cm}$ (Routine Patching: ₹1,500)
  * **Medium:** $30\text{ cm} \le \text{Width} \le 60\text{ cm}$ (Bituminous Filling: ₹4,500)
  * **High:** Width $> 60\text{ cm}$ (Hazardous Crater Reconstruction: ₹9,500)

### 3. Pan-India Jurisdiction Intelligence
* **Live Geocoding:** Reverse-geocodes GPS coordinates live using OpenStreetMap Nominatim.
* **Corridor Identification:** Resolves National Highways (`NH-XX`), State Highways (`SH-XX`), Expressways, and Municipal streets.
* **Warranty Classification:** Automatically applies 5-year EPC DLP clauses for NHAI highways, 3-year PWD clauses for state roads, and 2-year maintenance clauses for urban roads.

---

## 🚀 How to Run the Project

### Option 1: Live Cloud Application (Zero Setup)
Open the deployed production URL on any phone, tablet, or laptop:
👉 **[https://veridex-omega.vercel.app](https://veridex-omega.vercel.app)**

*Mobile Note:* Open on your smartphone browser (Chrome / Safari) to test with your phone's live rear/front camera and GPS.

---

### Option 2: Local Web Server (Development)
Run the multi-threaded dual-stack local server:

1. Clone the repository:
   ```bash
   git clone https://github.com/JaiBhaskar/Veridex.git
   cd Veridex
   ```
2. Start the local server:
   ```bash
   python serve.py
   ```
3. Open your browser:
   * **Local Access:** `http://localhost:8000`
   * **Local IP:** `http://127.0.0.1:8000`

---

### Option 3: Streamlit Companion Analytics Dashboard
For desktop data analytics and batch video processing:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch Streamlit:
   ```bash
   python -m streamlit run app.py
   ```

---

### Option 4: Deploying to Vercel (Production)
To deploy your own instance to Vercel in 1 command:
```bash
npx vercel --prod --yes
```

---

## 📱 How to Use the Application

1. **Start the Feed:**
   * **On Phone / Car Mount:** Tap **`📷 Use Camera`** (switch between front and rear cameras using **`🔄 Flip Camera`**).
   * **For Demo / Testing:** Tap **`🚗 Play Sample Video`** to run the pre-loaded 1080p highway test video.
2. **Begin Detection:**
   * Tap **`▶ Start Detecting`**.
   * The AI will render real-time neon bounding boxes, confidence tags, and metric width estimates over potholes.
3. **Inspect the Map:**
   * View defect locations plotted in real time on the **Esri World Street Map**.
   * Click any marker to view the pothole ID, width, road authority, and contractor liability.
4. **Indoor Demo Mode (Judges & Presentations):**
   * Tap **`⚡ Test Pothole`** to simulate an immediate defect detection on demand.
   * Demonstrates the audio alert beep, map pin drop, liability claim calculation, and legal notice generation without needing live road driving.
5. **Export & Legal Enforcement:**
   * Tap **`📋 Copy Notice`** to copy a formal legal Defect Liability repair enforcement notice.
   * Tap **`📥 Export CSV`** to download a clean, Excel-ready audit report (`.csv`) with UTF-8 encoding, exact GPS links, and total claim costs in ₹ INR.

---

## 📁 Repository Structure

```
├── index.html              # Main Production Edge Web App (ONNX Runtime Web, Esri Leaflet Map, Mobile HUD)
├── pothole.onnx            # Trained YOLOv8 Edge Vision Model (13.28 MB)
├── sample-road-video.mp4   # 1080p Real-World Road Test Footage
├── serve.py                # Multi-Threaded Dual-Stack Local Test Server (IPv4 + IPv6)
├── app.py                  # Streamlit Companion Analytics Dashboard
├── vercel.json             # Vercel Production Static Edge Configuration
├── .vercelignore           # Vercel Deployment Optimization Rules
├── manifest.json           # Progressive Web App (PWA) Manifest
├── requirements.txt        # Python Dependencies (Streamlit, ONNX Runtime, OpenCV)
└── package.json            # Node.js Project Metadata
```

---

## 📄 License
This project is developed for academic presentation, hackathons, and civic infrastructure monitoring. All rights reserved.
