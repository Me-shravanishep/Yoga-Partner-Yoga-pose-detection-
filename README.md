# Yoga Partner — Yoga Pose Detection

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
