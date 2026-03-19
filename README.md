# 🎥 Smart CCTV Surveillance System

## 📌 Overview

The **Smart CCTV Surveillance System** is an intelligent video monitoring solution built using **YOLO (You Only Look Once)** and **OpenCV**. It detects objects, monitors activities in real-time, and triggers alerts based on predefined rules.

This project is designed to enhance security by automating surveillance and reducing manual monitoring.

---

## 🚀 Features

* 🎯 Real-time object detection using YOLO
* 📹 Video stream processing (live or recorded)
* ⚠️ Custom alert system for suspicious activities
* 🧠 Rule-based detection logic
* 📊 Modular and scalable architecture

---

## 🛠️ Tech Stack

* **Python**
* **OpenCV**
* **YOLOv8**
* **NumPy**

---

## 📂 Project Structure

```
SmartCCTV_Project/
│── alert.py          # Handles alert triggering
│── config.py         # Configuration settings
│── detector.py       # Object detection logic
│── rules.py          # Custom surveillance rules
│── utils.py          # Helper functions
│── requirements.txt  # Dependencies
│── Videos/           # Input video files (ignored in Git)
│── Logs/             # Log files (ignored in Git)
```

---

## ⚙️ Installation

### 1. Clone the repository

```
git clone https://github.com/Janani-Works/SmartCCTV-surveillance.git
cd SmartCCTV-surveillance
```

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the main detection script:

```
python detector.py
```

---

## ⚠️ Notes

* Large files like models (`.pt`) and videos are excluded using `.gitignore`
* Ensure YOLO model weights are downloaded separately
* Modify rules in `rules.py` for custom behavior

---

## 📸 Future Improvements

* 📡 Live CCTV camera integration
* 🌐 Web dashboard for monitoring
* 🔔 Email/SMS alert system
* 🧠 AI-based anomaly detection

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repo and submit a pull request.

---

## 📄 License

This project is for educational purposes.

---

## 👩‍💻 Author

**Ponjanani**

---

## ⭐ Show your support

If you like this project, give it a ⭐ on GitHub!
