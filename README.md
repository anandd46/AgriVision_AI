<<<<<<< HEAD
# AgriVision AI: AI Agriculture Disease Detection & Guide

AgriVision AI is a modern, responsive, and farmer-focused web and API application built using **Python, Flask, and OpenCV**. It diagnoses critical diseases in **Coconut and Arecanut leaves** using real-time computer vision segmentation, provides organic and chemical treatment guides, calculates precise NPK fertilizer ratios, and offers ready-to-use API endpoints for mobile apps (Flutter / React Native).

---

## 🌟 Key Features

1. **Leaf Disease Diagnosis (Computer Vision)**:
   - Evaluates leaf health via advanced color space analysis (HSV thresholding) separating healthy green, chlorotic yellow, and necrotic brown areas.
   - Detects leaf spot anomalies and highlights them with **automatic bounding boxes** (simulating YOLOv8/CNN predictions).
   - Diagnoses:
     - **Coconut**: Leaf Rot, Bud Rot, Gray Leaf Spot.
     - **Arecanut**: Yellow Leaf Disease (YLD), Fruit Rot (Koleroga), Foot Rot (Anabe).
2. **Fertilizer Recommendation Calculator**:
   - Calculates custom Nitrogen (N), Phosphorus (P), Potassium (K), Lime, and organic manure dosages.
   - Scales nutrients based on **tree age** (from sapling to mature palm), **soil type** (loamy, sandy, laterite, clayey), and **disease state** (immune-booster mode).
3. **Foliar Encyclopedia (Disease Library)**:
   - Filterable library detailing symptom sheets, causes, and step-by-step organic/chemical treatment remedies.
4. **Mobile App REST API & Integration Guides**:
   - Includes `/api/scan` and `/api/fertilizer` endpoints.
   - Complete copy-pasteable integration snippets in **Dart (Flutter)** and **JavaScript (React Native)**.
5. **Modern Farmer-Friendly UI**:
   - Beautiful glassmorphic design system using forest green gradients.
   - Laser-scanning animation, progress gauges, and full light/dark mode support.
   - Highly responsive bottom-navigation design tailored for mobile screens in the field.

---

## 📁 Repository Structure

```text
E:\ANTIGRAVITY\Agri\
├── app.py                     # Flask Main Application & Routing
├── requirements.txt           # Python Package Dependencies
├── README.md                  # Installation & Developer Manual
├── models/
│   ├── __init__.py            # Python package entry
│   └── disease_detector.py    # CV Segmentation & Diagnostic Database
├── templates/
│   ├── base.html              # Core Layout & Bottom/Sidebar Navigation
│   ├── dashboard.html         # Weather, Alerts, & Tools Hub
│   ├── scan.html              # Leaf Upload, Laser Scanner & Diagnostic view
│   ├── fertilizer.html        # NPK dosage form & Progress Gauges
│   ├── library.html           # Searchable Fungal Disease Guide
│   └── api_docs.html          # Flutter / React Native Integration Manual
└── static/
    ├── css/
    │   └── style.css          # Glassmorphic dark/light CSS
    └── js/
        └── main.js            # AJAX scanner, themes, & animation scripts
```

---

## 🚀 Step-by-Step Installation Guide

### Prerequisites
Make sure you have **Python 3.8 or higher** installed on your system.

### 1. Open Terminal/PowerShell at the Project Location
Open your terminal (PowerShell, Command Prompt, or Bash) and navigate to the project directory:
```bash
cd E:\ANTIGRAVITY\Agri
```

### 2. Create a Virtual Environment (Recommended)
This isolates the project dependencies:
- **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Package Dependencies
Install the required packages using `pip`:
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Start the Flask development server:
```bash
python app.py
```

### 5. Access the Web App
Open your web browser and navigate to:
```text
http://127.0.0.1:5000
```
*Tip: If testing on a mobile device on the same local network, run `python app.py` and access the page using `http://<your-computer-ip-address>:5000`.*

---



## 🛠️ Scaling Up to Deep Learning (TensorFlow / YOLO)

The architecture is built with modularity in mind. If you want to connect a trained **TensorFlow/Keras CNN** model or **Ultralytics YOLO** detector later, simply drop the model file (e.g., `crop_disease_model.h5`) into the `models/` directory, install the libraries, and modify the shell inside `models/disease_detector.py`:

```python
# Install Tensorflow: pip install tensorflow
import tensorflow as tf

class DiseaseDetector:
    def __init__(self):
        # Load your CNN model weights here
        self.model = tf.keras.models.load_model('models/crop_disease_model.h5')

    def analyze_image(self, image_bytes, crop_hint):
        # 1. Preprocess image bytes (resize to match input shape, e.g., 224x224)
        # 2. Run prediction: self.model.predict(preprocessed_image)
        # 3. Return bounding boxes and classification indices
```

---

## 📱 Mobile REST API Integration Reference

### Leaf Disease Scanner API
- **Endpoint**: `/api/scan`
- **Method**: `POST`
- **Request Headers**: `Content-Type: multipart/form-data`
- **Request Parameters**:
  - `image`: Binary file (Leaf photo)
  - `crop`: String (`coconut` or `arecanut`)
- **JSON Response Format**:
  ```json
  {
    "crop": "Coconut",
    "disease_name": "Coconut Leaf Rot (Colletotrichum gloeosporioides)",
    "confidence": 94.0,
    "severity": "medium",
    "symptoms": ["Large decayed dry patches...", "Blackening of leaf tips"],
    "organic_treatment": "Apply Neem cake...",
    "chemical_treatment": "Spray Copper Oxychloride...",
    "fertilizer_recommendation": "Increase Potassium by 20%...",
    "metrics": {
      "green_percentage": 75.5,
      "yellow_percentage": 10.2,
      "brown_percentage": 14.3
    },
    "annotated_image": "data:image/jpeg;base64,..."
  }
  ```

*See the **Mobile API Docs** page in the web app for complete, copy-pasteable **Flutter (Dart)** and **React Native (JS)** camera upload functions.*
=======
# AgriVision_AI
>>>>>>> 5f64282f3793e0e2d0c2153b2da5e3678bd158db
