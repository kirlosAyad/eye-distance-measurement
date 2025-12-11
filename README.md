# 👁️ Eye Distance Measurement using MediaPipe  
### Real-Time Eye Distance Detection + Pixel-to-Centimeter Calibration

This project measures the **distance between the eyes in real time** using MediaPipe FaceMesh.  
A calibration step using a VISA/ID card (8.56 cm width) allows conversion of the measurement from **pixels to centimeters**.

---

## 🚀 Features
- Real-time facial landmark detection  
- Eye distance calculation (px + cm)  
- Manual calibration using two mouse clicks  
- Accurate scale conversion  
- Works on any webcam  

---

## 🧠 How It Works

### 🔹 1. Calibration  
The user clicks **two points** on a VISA/ID card (known width: 8.56 cm).  
The program calculates:
cm_per_pixel = 8.56 / pixel_distance

### 🔹 2. Eye Measurement  
MediaPipe FaceMesh landmarks:  
- Right eye → point 33  
- Left eye → point 263  

Distance formula:
eye_cm = eye_px * cm_per_pixel


Displayed live on screen.

---

## 📦 Requirements

Install dependencies:
pip install -r requirements.txt

---

## ▶️ Run the Project
python eye_distance.py


Steps:
1. Hold VISA/ID card horizontally  
2. Click left and right edges of the card  
3. Calibration completes  
4. Eye distance appears (px + cm)

---

## 🖼 Example Image

![eye-distance-image](A_digital_photograph_captures_a_close-up_portrait_.png)

---

## 👨‍💻 Author  
**Krollos Ayad** – AI & ML Engineer  

