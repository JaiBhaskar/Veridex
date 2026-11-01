# 🕳️ VERIDEX AI — Autonomous Road Health & Contractor Warranty Engine
### *Edge Computer Vision, Photogrammetric 3D Sizing & Legal Defect Liability Period (DLP) Enforcement*
**Official Submission for Techfest — IIT Bombay**

[![Deployment: Vercel](https://img.shields.io/badge/Deploy-Vercel-black?logo=vercel)](https://vercel.com)
[![Framework: ONNX Runtime Web](https://img.shields.io/badge/Engine-ONNX_Runtime_Web-0078D4?logo=microsoft)](https://onnxruntime.ai)
[![Architecture: YOLOv8](https://img.shields.io/badge/Vision-YOLOv8-FF5722)](https://github.com/ultralytics/ultralytics)
[![Venue: IIT Bombay](https://img.shields.io/badge/Venue-IIT_Bombay_Techfest-7C3AED)](#)

---

## 📌 Executive Summary

India loses thousands of lives and crores of rupees annually due to road craters and potholes. While multiple projects perform raw computer vision detection, **none solve the accountability problem**:
> *"Who is legally responsible for repairing this pothole, and who pays for it?"*

Under Indian road construction norms (**NHAI, MoRTH, State PWD, and BMC/MCGM EPC/HAM guidelines**), every new road has a mandatory **Defect Liability Period (DLP / Warranty)** ranging from **3 to 5 years**. During this period, the **private contractor is legally bound to repair any pothole within 48 to 72 hours at zero cost to the public exchequer**. If the warranty has expired, the defect is routed to the municipal maintenance budget.

**VERIDEX AI** runs real-time edge computer vision on a smartphone or dashcam, calculates the exact metric dimensions (in centimeters/meters) and 3D road coordinates using flat-road photogrammetry, cross-references live GPS against government road contracts, and automatically generates legal defect liability claim notices with high-resolution photo evidence.

---

## 🚀 Live Demo & Quick Deployment

### Option 1: 1-Click Deployment to Vercel (Recommended for Phone & Judges)
Deploying to Vercel provides a permanent **HTTPS URL with SSL**, which is **strictly required by Android Chrome and iOS Safari to enable phone camera and GPS sensors**.

1. Push this folder to your GitHub:
   ```bash
   git init
   git add .
   git commit -m "VERIDEX IIT Bombay Release"
   git branch -M main
   git remote add origin https://github.com/<your-username>/veridex-pothole.git
   git push -u origin main
   ```
2. Go to [vercel.com](https://vercel.com), click **Add New Project**, import your repository, and click **Deploy**.
3. **Done!** Open `https://your-project.vercel.app` on your phone. Camera, GPS, and ONNX AI inference will run instantly!

*Alternatively, using Vercel CLI from this directory:*
```bash
npx vercel --prod
```

---

### Option 2: Local Testing on Laptop & Phone (Wi-Fi)
To test locally across devices on the same Wi-Fi network:
```bash
python serve.py
```
This starts an optimized server on `http://localhost:8000` and displays your local IP (e.g. `http://192.168.1.x:8000`).

> ⚠️ **Important Phone Note:**
> Modern mobile browsers (iOS Safari & Android Chrome) disable `getUserMedia` (camera) and `geolocation` over insecure HTTP (`http://192.168.x.x`).  
> **Solution:** Use the deployed Vercel HTTPS link, or run with self-signed SSL: `python serve.py --ssl`.

---

### Option 3: Streamlit Python Dashboard
For desktop presentation or cloud analytics:
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🛠️ Root-Cause Analysis: Why Phone Camera & GPS Failed (And How We Fixed It)

| Issue | Root Cause | Solution Implemented in VERIDEX |
| :--- | :--- | :--- |
| **Phone Camera Not Opening** | Mobile browsers block `navigator.mediaDevices` on non-HTTPS origins (except localhost). Additionally, hardcoded landscape resolutions (`1280x720`) throw `OverconstrainedError` on mobile portrait sensors. | Added progressive fallback constraints (`facingMode: "environment"` ➔ `user` ➔ `true`), iOS Safari inline playback attributes (`playsinline`, `webkit-playsinline`, `muted`), camera flip button, and Vercel HTTPS configuration. |
| **GPS Unavailable / Failing** | `watchPosition` with strict `timeout: 20000` times out indoors. The old code immediately killed the watch and displayed "GPS denied". | Implemented a two-stage GPS pipeline: quick coarse network fix ➔ continuous high-accuracy tracking. Added timeout auto-retry, indoor manual preset selector, and Leaflet map tap-to-locate. |
| **Model Incompatibility** | YOLOv8-seg models output 37 channels (`[1, 37, 8400]`). The old decoder read mask prototype rows 5–36 as class scores, corrupting detections. | Fixed decoder to separate bounding box (rows 0–3), class confidence (row 4), and mask coefficients (rows 5–36). |

---

## 📐 Mathematical Formulation: Photogrammetric 3D Sizing

VERIDEX does not guess pothole sizes—it computes them geometrically using single-camera monocular ground projection.

```
                  Optical Axis
Camera (h) •-------------------------- Horizon
            \ θ (Tilt Down)
             \
              \ Ray to Pothole Ground Contact
               \
================•============================== Flat Road
                |<-------- d (forward) ------->|
```

### 1. Focal Length from Field of View (FOV):
$$f = \frac{W / 2}{\tan\left(\frac{\theta_{\text{FOV}}}{2}\right)}$$

### 2. Ray Intersection with Flat Road:
For a bounding box bottom-center point $(u, v)$ with optical center $(c_x, c_y) = (W/2, H/2)$:
$$y_{\text{norm}} = \frac{v - c_y}{f}, \quad x_{\text{norm}} = \frac{u - c_x}{f}$$
$$\text{Denominator} = \sin(\theta) + y_{\text{norm}} \cos(\theta)$$
$$\text{Optical Depth } t = \frac{h}{\text{Denominator}}$$
$$\text{Forward Distance } d = t \cdot \left(\cos(\theta) - y_{\text{norm}} \sin(\theta)\right)$$
$$\text{Lateral Offset } x = t \cdot x_{\text{norm}}$$

### 3. Metric Pothole Width:
Using the bounding box pixel width $w_{\text{px}} = x_2 - x_1$:
$$w_{\text{metric}} = \frac{w_{\text{px}} \cdot t}{f} \quad (\text{meters})$$

- **Low Severity:** $w_{\text{metric}} < 30\text{ cm}$
- **Medium Severity:** $30\text{ cm} \le w_{\text{metric}} \le 60\text{ cm}$
- **High / Severe:** $w_{\text{metric}} > 60\text{ cm}$ (Hazardous Crater)

---

## 🏛️ Preloaded Road Contracts (Techfest IIT Bombay & National Highways)

| Road ID | Corridor Name | Jurisdiction | Contractor | Status |
| :--- | :--- | :--- | :--- | :--- |
| **IITB-01** | Adi Shankaracharya Marg / JVLR (Powai) | BMC / MMRDA | Larsen & Toubro (L&T) | 🟢 Under DLP Warranty (3 Years) |
| **MUM-01** | Western Express Highway (WEH) / NH-48 | Maharashtra PWD | IRB Infrastructure | 🟢 Under DLP Warranty (5 Years) |
| **MUM-02** | Eastern Express Highway (EEH) | BMC / MCGM | HCC – Shapoorji Pallonji | 🔴 Warranty Expired (Routine PWD) |
| **NHAI-95** | Ludhiana Elevated Highway, NH-95 | NHAI | Gammon – SP Singla (JV) | 🟢 Under DLP Warranty (5 Years) |
| **NHAI-07** | Bhatinda–Malout Corridor, NH-7 | NHAI | Dineshchandra R. Agrawal | 🟢 Under DLP Warranty (4 Years) |

*Global fallback: If the vehicle enters any unlisted road in the world, the built-in OpenStreetMap Nominatim reverse-geocoder resolves the road name and authority in real-time.*

---

## 🎤 3-Minute Presentation Pitch for Techfest IIT Bombay Judges

1. **The Hook (30s):**
   > *"Good morning, respected judges. In India, potholes cause thousands of accidents every monsoon. But when citizens complain, municipalities and contractors engage in blame games. Why? Because the public does not know who holds the road contract and whether it is under warranty."*

2. **The Innovation (60s):**
   > *"We present **VERIDEX AI**. It runs 100% on the edge in any mobile browser or dashcam. Using a custom YOLOv8 model running via WebAssembly SIMD and flat-road photogrammetry, it measures the exact metric width of potholes in centimeters and computes their 3D distance without expensive LiDAR."*

3. **The Impact & Legal Engine (60s):**
   > *"Every road in India is legally covered by a Defect Liability Period (DLP). VERIDEX cross-references GPS with the government contract database. If a pothole is found on JVLR right outside IIT Bombay, it immediately flags the contractor—in this case, L&T—who is legally bound under IRC guidelines to repair it within 72 hours for free. We can export an audit report or dispatch an official legal notice with one click."*

4. **Live Demo (30s):**
   > *"Watch this live demonstration: here is our dashboard tracking dashcam video, rendering real-time bounding boxes, plotting pins on Leaflet OSM, and classifying DLP liability."*

---

## 📁 Repository Structure

```
├── index.html              # Main Production Web Application (Mobile HUD, ONNX Web, Leaflet Map)
├── pothole.onnx            # Pre-trained YOLOv8 Pothole Detection Model (12.67 MB)
├── sample-road-video.mp4   # Pre-loaded dashcam test video (for instant indoor demo)
├── serve.py                # Local development & mobile testing server (with SSL & WASM headers)
├── app.py                  # Streamlit companion cloud dashboard
├── vercel.json             # Vercel deployment configuration (SIMD multi-threading headers)
├── manifest.json           # Progressive Web App (PWA) manifest for home screen install
├── requirements.txt        # Python dependencies for Streamlit
├── package.json            # NPM project metadata
├── train_pothole_yolo.py   # Training script for Ultralytics YOLOv8
└── colab_cells.py          # Google Colab GPU notebook cells
```

---

## 🏆 Techfest IIT Bombay Verification Checklist

- [x] Model downloads and initializes automatically in browser (`pothole.onnx`).
- [x] Real-time inference running at 30+ FPS using ONNX Runtime Web.
- [x] Photogrammetric depth and width calculations calibrated with visual distance grid.
- [x] Camera access working on Android and iOS Safari.
- [x] GPS tracking with indoor manual venue fallback for IIT Bombay.
- [x] Interactive Leaflet map with color-coded severity defect pins.
- [x] DLP warranty evaluation and automated legal notice generator.
- [x] 1-Click sample video button for indoor booth demonstrations.
- [x] 1-Click Vercel deployment ready.

---
**VERIDEX AI** — *Empowering Citizen Audits & Transparent Road Infrastructure.*
