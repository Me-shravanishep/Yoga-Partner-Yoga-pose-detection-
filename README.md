# 🧘 Yoga Pose Detection

Real-time yoga pose detection using MediaPipe and OpenCV with Flask web interface.

## 🚀 Quick Start

```powershell
# 1. Navigate to project
cd "c:\Users\shrav\OneDrive\Desktop\YOGA POSE DETECTION\Yoga-Partner-Yoga-pose-detection-"

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Run the app
python app.py
```

Open browser: **http://127.0.0.1:5000**

## 📋 First Time Setup

```powershell
# Install Python 3.11.9
# Download: https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe

# Create virtual environment
py -3.11 -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run
python app.py
```

## 🎮 Features

- **Real-time pose detection** with 33 body landmarks
- **Skeleton overlay** on webcam feed
- **User registration** system (saves to `data/` folder)
- **Pose classification** for yoga poses
- **REST API** endpoints for integration

## 🎯 Usage

- Press **S** to start camera
- Press **X** to stop camera
- Fill form and click "Save User" to register
- Click "Test Health" to check system status

## 📁 Project Structure

```
├── app.py                  # Main Flask application
├── requirements.txt        # Dependencies
├── models/
│   └── pose_detector.py   # Pose detection logic
├── templates/
│   └── index.html         # Web interface
├── static/
│   ├── css/style.css      # Styling
│   └── js/main.js         # Frontend logic
└── data/                  # User data storage
```

## 🛠️ Tech Stack

- **Flask** - Web framework
- **MediaPipe** - Pose detection (33 landmarks)
- **OpenCV** - Video capture and processing
- **NumPy** - Mathematical operations

## ⚠️ Requirements

- Python 3.11 (MediaPipe doesn't support 3.13)
- Webcam
- Windows/Linux/Mac

## 📊 API Endpoints

- `GET /` - Main page
- `GET /health` - System health check
- `GET /video_feed` - MJPEG video stream
- `POST /api/save_user` - Save user data
- `GET /api/get_users` - Retrieve all users

## 🐛 Troubleshooting

**Camera not working?** Close other apps using camera (Zoom, Teams, etc.)

**Module not found?** Activate virtual environment: `.\venv\Scripts\Activate.ps1`

**Port in use?** Stop other Flask apps or change port in `app.py`

This repository will host a web app that performs yoga pose detection using OpenCV and MediaPipe.

This initial scaffold includes a minimal Flask app that lets you verify OpenCV and MediaPipe are installed and provides a very small test endpoint which captures a single frame from the default webcam (if available).

Note about Python version

MediaPipe distributes prebuilt wheels for specific Python versions. If you have Python 3.13 (or another very new interpreter) you may see "No matching distribution found for mediapipe" when installing requirements. Use Python 3.10 or 3.11 to avoid that problem.

Quick start (Windows PowerShell)

1. Create and activate a virtual environment:

	```powershell
	python -m venv venv
	.\venv\Scripts\Activate.ps1
	```

2. Install dependencies:

	```powershell
	pip install --upgrade pip
	pip install -r requirements.txt
	```

3. Run the app:

	```powershell
	python app.py
	```

4. Open http://127.0.0.1:5000/ in your browser. A simple health endpoint is available at /health which reports installed OpenCV and MediaPipe versions. A single-frame webcam capture is available at /capture (works if the server has a webcam and permissions).

What's next

- Extend the Flask app to stream webcam frames to the front-end or accept uploaded videos.
- Add MediaPipe Pose processing and a client-side overlay to show keypoints.
- Add a classification model or heuristic to map keypoints to known yoga poses.

If you'd like, I can now add a live streaming endpoint that sends MJPEG frames and a small client page that draws MediaPipe keypoints on a canvas.

Team: CODEASTRA
# Yoga-Partner-Yoga-pose-detection-
TEAM CODEASTRA
