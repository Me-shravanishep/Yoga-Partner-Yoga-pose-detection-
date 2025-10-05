# Quick Start Guide - Yoga Pose Detection

## Step-by-Step Setup (Windows)

### 1. Check Python Version

```powershell
python --version
# Should show Python 3.10.x or 3.11.x
```

If you don't have Python 3.10/3.11, download from:
- https://www.python.org/downloads/
- Or use Microsoft Store

### 2. Navigate to Project Directory

```powershell
cd "C:\Users\shrav\OneDrive\Desktop\YOGA POSE DETECTION\Yoga-Partner-Yoga-pose-detection-"
```

### 3. Run the Setup Script

```powershell
# If you have py launcher (recommended)
.\setup.ps1 -Python "py -3.10"

# OR if you know the exact python path
.\setup.ps1 -Python "C:\Python310\python.exe"

# OR just use default python
.\setup.ps1
```

This will:
- Create a virtual environment in `venv/`
- Upgrade pip
- Install all requirements (Flask, OpenCV, MediaPipe, NumPy, pyttsx3)

### 4. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` at the beginning of your prompt.

**Note:** If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 5. Verify Installation

```powershell
python -c "import cv2, mediapipe, flask, numpy; print('All libraries installed successfully!')"
```

### 6. Run the Application

```powershell
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```

### 7. Open in Browser

Visit: http://127.0.0.1:5000/

You should see the Yoga Pose Detection interface!

---

## Testing the Features

### Test 1: Health Check
Visit: http://127.0.0.1:5000/health

Should return JSON with library versions.

### Test 2: Camera Test
Visit: http://127.0.0.1:5000/capture

Should return your camera resolution if camera is detected.

### Test 3: Live Detection
On the main page, click **"Start Detection"** button.

You should see:
- Your webcam feed
- Blue/pink skeleton overlay showing detected pose landmarks
- Real-time tracking

### Test 4: Save User
Fill out the user registration form and click "Save User".

Check the `data/` folder for a new JSON file with your data.

---

## Keyboard Shortcuts

- Press `S` - Start video detection
- Press `X` - Stop video detection

---

## Troubleshooting

### Problem: MediaPipe won't install
**Solution:**
- Make sure you're using Python 3.10 or 3.11
- Try: `pip install mediapipe==0.10.0` specifically

### Problem: Camera not detected
**Solution:**
- Make sure no other app is using the camera
- Check Windows camera privacy settings
- Try changing camera index in app.py: `cv2.VideoCapture(1)` instead of `(0)`

### Problem: Flask won't start
**Solution:**
- Make sure port 5000 is not in use
- Check if venv is activated (you should see `(venv)` in prompt)
- Try: `python -m flask run`

### Problem: Cannot activate venv (execution policy)
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Next Steps

1. **Explore the code:**
   - `app.py` - Main Flask routes
   - `models/pose_detector.py` - Pose detection logic
   - `static/js/main.js` - Frontend JavaScript
   - `templates/index.html` - HTML structure

2. **Customize:**
   - Add more yoga poses to `pose_detector.py`
   - Modify CSS in `static/css/style.css`
   - Add new routes in `app.py`

3. **Extend features:**
   - Add voice feedback (pyttsx3 is already installed)
   - Implement pose accuracy scoring
   - Add workout session tracking
   - Create a dashboard for saved users

---

## Stopping the Server

Press `Ctrl + C` in the terminal where Flask is running.

---

## Deactivating Virtual Environment

```powershell
deactivate
```

---

## Need Help?

Read:
- `PROJECT_README.md` - Full documentation
- `models/README.md` - Pose detection details
- Flask docs: https://flask.palletsprojects.com/
- MediaPipe docs: https://google.github.io/mediapipe/

**Happy Coding! 🚀**
