<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/YOLOv8-Fine--Tuned-00FFFF?style=flat" alt="YOLOv8">
  <img src="https://img.shields.io/badge/Ultralytics-8.2+-111F68?style=flat" alt="Ultralytics">
  <img src="https://img.shields.io/badge/OpenCV-4.10-5C3EE8?style=flat&logo=opencv" alt="OpenCV">
  <img src="https://img.shields.io/badge/Streamlit-1.36-FF4B4B?style=flat&logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/FastAPI-Web%20Inference-009688?style=flat&logo=fastapi" alt="FastAPI">
</p>

# Tomato Ripeness Classification

<p align="center">
  <img src="https://img.shields.io/badge/Task-Object%20Detection%20%2B%20Ripeness%20Classification-2EA44F?style=for-the-badge" alt="Task">
  <img src="https://img.shields.io/badge/Model-YOLOv8m%20Fine--Tuned-111F68?style=for-the-badge" alt="Model">
  <img src="https://img.shields.io/badge/Best%20mAP50-0.881-2EA44F?style=for-the-badge" alt="mAP50">
  <img src="https://img.shields.io/badge/Best%20mAP50--95-0.777-2EA44F?style=for-the-badge" alt="mAP50-95">
</p>

A computer vision system for **tomato detection and ripeness classification** using a fine-tuned YOLOv8 model. The project detects tomatoes in images, uploaded videos, webcam feeds, RTSP streams, and YouTube video streams, then classifies each tomato into one of six ripeness categories.

The system includes a Streamlit application for interactive inference, YOLOv8 training/evaluation artifacts, and an additional FastAPI-based inference layout for image, video, and live-feed processing.

**Developer:** Lasantha Kulasooriya

---

<p align="center">
  <img src="https://img.shields.io/badge/Table%20of%20Contents-Overview%20%7C%20Demo%20%7C%20Training%20%7C%20Metrics%20%7C%20Usage-green?style=flat-square" alt="Table of Contents">
</p>

- [Tomato Ripeness Classification](#tomato-ripeness-classification)
  - [Overview](#overview)
  - [Demo](#demo)
    - [Application UI](#application-ui)
    - [Prediction Output](#prediction-output)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [Model Classes](#model-classes)
  - [Dataset](#dataset)
  - [Model Fine-Tuning](#model-fine-tuning)
  - [Evaluation Results](#evaluation-results)
    - [Best Model](#best-model)
    - [Model Comparison](#model-comparison)
    - [Per-Class Evaluation](#per-class-evaluation)
  - [Visual Evaluation Artifacts](#visual-evaluation-artifacts)
    - [Training Results](#training-results)
    - [Confusion Matrix](#confusion-matrix)
    - [Normalized Confusion Matrix](#normalized-confusion-matrix)
    - [Precision-Recall Curve](#precision-recall-curve)
    - [F1 Confidence Curve](#f1-confidence-curve)
    - [Precision Curve](#precision-curve)
    - [Recall Curve](#recall-curve)
  - [Application Workflow](#application-workflow)
  - [Installation](#installation)
  - [Run Streamlit App](#run-streamlit-app)
  - [FastAPI Inference Layout](#fastapi-inference-layout)
  - [Notes on Large Files](#notes-on-large-files)
  - [Developer](#developer)

---

## Overview

This project fine-tunes YOLOv8 for tomato ripeness detection. Instead of only classifying an entire image, the model localizes each tomato with a bounding box and assigns a ripeness class to each detected object.

The final application supports:

- Still-image tomato detection
- Uploaded video inference
- Webcam inference
- RTSP stream inference
- YouTube video stream inference
- Object tracking using Ultralytics tracker configurations
- Streamlit-based interactive model testing
- FastAPI-style inference modules for web-based deployment experiments

---

## Demo

### Application UI

<p align="center">
  <img src="./app2/app%20UI.png" alt="Tomato Classification Streamlit App UI" width="850">
</p>

### Prediction Output

<p align="center">
  <img src="./tmto/src/runs/detect/predict/IMG_0991.jpg" alt="Tomato Ripeness Prediction Output" width="700">
</p>

---

## Features

<p align="left">
  <img src="https://img.shields.io/badge/Fine--Tuned-YOLOv8m-blue" alt="Fine Tuned YOLOv8m">
  <img src="https://img.shields.io/badge/Inference-Image%20%7C%20Video%20%7C%20Webcam-green" alt="Inference Sources">
  <img src="https://img.shields.io/badge/Streaming-RTSP%20%7C%20YouTube-orange" alt="Streaming">
  <img src="https://img.shields.io/badge/Tracking-ByteTrack%20%7C%20BoT--SORT-lightgrey" alt="Tracking">
</p>

| Feature | Description |
|---|---|
| **Fine-tuned detector** | YOLOv8 model fine-tuned for tomato ripeness detection across six classes |
| **Object-level classification** | Detects multiple tomatoes in one frame and classifies each bounding box |
| **Interactive UI** | Streamlit app with configurable confidence threshold |
| **Multi-source inference** | Supports images, uploaded videos, webcam, RTSP streams, and YouTube video streams |
| **Tracking support** | Uses Ultralytics tracking options such as ByteTrack and BoT-SORT |
| **Evaluation artifacts** | Includes training curves, PR/F1/P/R curves, confusion matrices, and validation outputs |
| **Deployment experiment** | Includes a FastAPI inference layout for image, video, and live-feed endpoints |

---

## Project Structure

```text
Tomato Ripeness Classification/
├── app2/
│   ├── app.py                  # Main Streamlit application
│   ├── helper.py               # YOLO loading, image/video/stream inference helpers
│   ├── settings.py             # Source and model path configuration
│   ├── requirements.txt        # Python dependencies
│   ├── images/                 # Demo images
│   ├── assets/                 # UI/demo assets
│   └── weights/                # Local model weights, ignored by git
├── tmto/
│   ├── data/
│   │   ├── dataset.yaml        # YOLO dataset configuration
│   │   └── annotations/        # COCO annotation exports
│   ├── src/
│   │   ├── model.ipynb         # Model fine-tuning notebook
│   │   └── runs/detect/        # YOLO training/evaluation outputs
│   └── webapp/
│       ├── app/                # FastAPI inference modules
│       ├── static/
│       └── templates/
├── .gitignore
└── README.md
```

---

## Model Classes

The model predicts six tomato ripeness classes:

| Class ID | Class Name | Meaning |
|---:|---|---|
| 0 | `b_fully_ripened` | Big fully ripened tomato |
| 1 | `b_half_ripened` | Big half ripened tomato |
| 2 | `b_green` | Big green tomato |
| 3 | `l_fully_ripened` | Little/small fully ripened tomato |
| 4 | `l_half_ripened` | Little/small half ripened tomato |
| 5 | `l_green` | Little/small green tomato |

Dataset configuration:

```yaml
names:
  - b_fully_ripened
  - b_half_ripened
  - b_green
  - l_fully_ripened
  - l_half_ripened
  - l_green
nc: 6
path: ../
train: ../data/train/images
val: ../data/val/images
```

---

## Dataset

The dataset annotations are available as COCO-style JSON files and were converted/used for YOLO training.

| Split | Images | Tomato Instances |
|---|---:|---:|
| Train | 643 | 7,781 |
| Validation/Test | 161 | 1,996 |

Validation/test class distribution:

| Class | Instances |
|---|---:|
| `b_fully_ripened` | 72 |
| `b_half_ripened` | 116 |
| `b_green` | 387 |
| `l_fully_ripened` | 269 |
| `l_half_ripened` | 223 |
| `l_green` | 929 |

---

## Model Fine-Tuning

Two YOLOv8 model variants were trained and compared:

| Run | Base Model | Epochs | Image Size | Batch Size |
|---|---|---:|---:|---:|
| `train` | YOLOv8s | 100 | 640 | 16 |
| `train2` | YOLOv8m | 100 | 640 | 16 |

The best model was produced by the `train2` run using **YOLOv8m**.

Training configuration highlights:

| Parameter | Value |
|---|---:|
| Task | Detection |
| Epochs | 100 |
| Image size | 640 |
| Batch size | 16 |
| Optimizer | AdamW, selected by Ultralytics auto optimizer |
| Pretrained transfer | 469/475 items transferred |
| Validation | Enabled |
| Tracker config | BoT-SORT available |

YOLOv8m model summary from the training notebook:

| Property | Value |
|---|---:|
| Layers | 295 |
| Parameters | 25,859,794 |
| Gradients | 25,859,778 |
| Compute | 79.1 GFLOPs |
| Fused layers | 218 |
| Fused parameters | 25,843,234 |
| Fused compute | 78.7 GFLOPs |
| Training duration | 6 hours, 58 minutes, 14.76 seconds |

---

## Evaluation Results

### Best Model

Best checkpoint:

```text
tmto/src/runs/detect/train2/weights/best.pt
```

Best epoch: **70**

| Metric | Value |
|---|---:|
| Precision | `0.84444` |
| Recall | `0.80188` |
| mAP50 | `0.88113` |
| mAP50-95 | `0.77693` |
| Validation box loss | `0.52421` |
| Validation class loss | `0.44464` |
| Validation DFL loss | `0.89975` |

### Model Comparison

| Run | Model | Best Epoch | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---:|---:|---:|---:|---:|
| `train` | YOLOv8s | 85 | `0.80296` | `0.82447` | `0.87513` | `0.76243` |
| `train2` | YOLOv8m | 70 | `0.84444` | `0.80188` | `0.88113` | `0.77693` |

YOLOv8m achieved the best overall result, improving mAP50-95 from `0.76243` to `0.77693` compared with the YOLOv8s run.

### Per-Class Evaluation

Per-class metrics from the best YOLOv8m checkpoint:

| Class | Images | Instances | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|---:|
| all | 161 | 1,996 | `0.844` | `0.802` | `0.881` | `0.777` |
| `b_fully_ripened` | 40 | 72 | `0.840` | `0.804` | `0.837` | `0.777` |
| `b_half_ripened` | 52 | 116 | `0.799` | `0.741` | `0.863` | `0.763` |
| `b_green` | 71 | 387 | `0.908` | `0.868` | `0.945` | `0.839` |
| `l_fully_ripened` | 59 | 269 | `0.825` | `0.821` | `0.886` | `0.787` |
| `l_half_ripened` | 67 | 223 | `0.800` | `0.740` | `0.848` | `0.735` |
| `l_green` | 69 | 929 | `0.891` | `0.836` | `0.908` | `0.758` |

---

## Visual Evaluation Artifacts

### Training Results

<p align="center">
  <img src="./tmto/src/runs/detect/train2/results.png" alt="YOLOv8m Training Results" width="850">
</p>

### Confusion Matrix

<p align="center">
  <img src="./tmto/src/runs/detect/train2/confusion_matrix.png" alt="Confusion Matrix" width="700">
</p>

### Normalized Confusion Matrix

<p align="center">
  <img src="./tmto/src/runs/detect/train2/confusion_matrix_normalized.png" alt="Normalized Confusion Matrix" width="700">
</p>

### Precision-Recall Curve

<p align="center">
  <img src="./tmto/src/runs/detect/train2/PR_curve.png" alt="Precision Recall Curve" width="700">
</p>

### F1 Confidence Curve

<p align="center">
  <img src="./tmto/src/runs/detect/train2/F1_curve.png" alt="F1 Confidence Curve" width="700">
</p>

### Precision Curve

<p align="center">
  <img src="./tmto/src/runs/detect/train2/P_curve.png" alt="Precision Curve" width="700">
</p>

### Recall Curve

<p align="center">
  <img src="./tmto/src/runs/detect/train2/R_curve.png" alt="Recall Curve" width="700">
</p>

---

## Application Workflow

```text
Input Source
  ├── Image upload
  ├── Video upload
  ├── Webcam
  ├── RTSP stream
  └── YouTube video stream
        ↓
YOLOv8 Model Loading
        ↓
Confidence Threshold Selection
        ↓
Frame/Image Preprocessing
        ↓
Tomato Detection + Ripeness Classification
        ↓
Optional Object Tracking
        ↓
Annotated Output Rendering
        ↓
Streamlit UI Display
```

The Streamlit application loads the trained YOLO model from `app2/weights/tmto_model.pt`, accepts a user-selected input source, applies the confidence threshold selected from the sidebar, and renders annotated detections back to the interface.

---

## Installation

Create and activate a virtual environment:

```bash
cd "/home/lasa/Desktop/Projects/Tomato Ripeness Classification"

python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r app2/requirements.txt
```

Core dependencies include:

| Library | Purpose |
|---|---|
| `ultralytics` | YOLOv8 training and inference |
| `torch`, `torchvision` | Deep learning backend |
| `opencv-python` | Video, webcam, RTSP, and frame processing |
| `streamlit` | Interactive application UI |
| `Pillow` | Image loading and display |
| `yt-dlp` | YouTube video stream extraction |
| `pandas`, `matplotlib`, `seaborn` | Evaluation analysis and visualization |

---

## Run Streamlit App

From the project root:

```bash
cd app2
streamlit run app.py
```

Then open the local Streamlit URL in the browser.

The sidebar allows:

- Model confidence threshold selection
- Input source selection
- Image upload
- Video upload
- Webcam inference
- RTSP stream inference
- YouTube stream inference
- Tracker selection for supported video sources

---

## FastAPI Inference Layout

The project also contains a FastAPI-oriented inference structure under:

```text
tmto/webapp/
```

Main modules:

| File | Purpose |
|---|---|
| `tmto/webapp/app/main.py` | FastAPI app, upload endpoints, websocket endpoint |
| `tmto/webapp/app/predict.py` | YOLO model loading and image/video/live-frame processing |
| `tmto/webapp/templates/index.html` | Web interface template |
| `tmto/webapp/static/` | Static assets and upload location |

This layout was used as a deployment experiment for serving image, video, and live-feed inference through API endpoints.

---

## Notes on Large Files

The repository contains generated ML artifacts that should not be committed to source control:

- Model weights: `*.pt`, `*.onnx`, `*.engine`, `*.h5`, `*.tflite`
- Training outputs: `runs/`
- Video files: `*.mp4`, `*.avi`, `*.mov`, `*.mkv`
- Runtime uploads: `static/uploads/`
- Dataset image splits and caches

These files are excluded through `.gitignore`. If the model weights are not included in a cloned copy, place the trained model at:

```text
app2/weights/tmto_model.pt
```

or update the model path in:

```text
app2/settings.py
```

---

## Developer

**Lasantha Kulasooriya**

