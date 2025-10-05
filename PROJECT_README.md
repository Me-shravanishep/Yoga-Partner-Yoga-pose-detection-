# 🧘 Yoga Pose Detection Web Application

A real-time yoga pose detection system powered by **MediaPipe**, **OpenCV**, and **Flask**. This application detects body landmarks, tracks poses, and provides visual feedback for yoga practitioners.

**Team:** CODEASTRA

---

## 📋 Features

- ✅ Real-time pose detection using MediaPipe Pose
- ✅ Live video streaming with pose landmark overlay
- ✅ User registration and data management
- ✅ REST API endpoints for integration
- ✅ Responsive web interface
- ✅ Pose angle calculation and classification
- ✅ Health monitoring and system status

---

## 🏗️ Project Structure

```
Yoga-Partner-Yoga-pose-detection-/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── setup.ps1                  # Windows setup script
│
├── static/                    # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css         # Application styles
│   ├── js/
│   │   └── main.js           # Frontend JavaScript
│   ├── images/               # Image assets
│   └── uploads/              # Uploaded files
│
├── templates/                 # HTML templates
│   └── index.html            # Main page
│
├── models/                   # Pose detection models
│   ├── pose_detector.py     # PoseDetector class
│   └── README.md            # Model documentation
│
├── data/                     # User data storage (JSON)
│   └── sample_data.json     # Sample data structure
│
└── venv/                     # Virtual environment (not in git)
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10 or 3.11** (recommended for MediaPipe compatibility)
- **Webcam** (for live pose detection)
- **Windows PowerShell** (for setup script)

### Installation

#### Option 1: Using Setup Script (Recommended)

```powershell
# Clone the repository
git clone <repository-url>
cd Yoga-Partner-Yoga-pose-detection-

# Run setup script with Python 3.10
.\setup.ps1 -Python "py -3.10"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the application
python app.py
```

#### Option 2: Manual Setup

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Access the Application

Open your browser and navigate to:
- **Main App:** http://127.0.0.1:5000/
- **Health Check:** http://127.0.0.1:5000/health
- **Video Stream:** http://127.0.0.1:5000/video_feed

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main landing page |
| GET | `/health` | System health and library versions |
| GET | `/capture` | Single frame capture test |
| GET | `/video_feed` | Live MJPEG video stream with pose detection |
| POST | `/api/save_user` | Save user data to JSON |
| GET | `/api/get_users` | Retrieve all saved users |

### Example API Usage

**Save User:**
```javascript
fetch('/api/save_user', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        name: "John Doe",
        age: 30,
        experience: "intermediate"
    })
})
```

**Get Users:**
```javascript
fetch('/api/get_users')
    .then(response => response.json())
    .then(data => console.log(data.users));
```

---

## 🧠 How It Works

### 1. Pose Detection Pipeline

```
Camera Feed → OpenCV Capture → MediaPipe Pose → Landmark Detection → 
Angle Calculation → Pose Classification → Visual Feedback
```

### 2. Key Components

- **MediaPipe Pose**: Detects 33 body landmarks in real-time
- **OpenCV**: Handles video capture and image processing
- **Flask**: Serves web interface and REST API
- **JavaScript**: Manages frontend interactions

### 3. Pose Classification

The system uses landmark coordinates to:
- Calculate joint angles (shoulder, elbow, knee, etc.)
- Compare angles with known yoga poses
- Classify poses (Mountain, Warrior, Tree, etc.)

---

## 📚 Learning Guide

### For Beginners

1. **Start with Flask Basics:**
   - Understand routes and templates (`app.py`)
   - Learn about request/response handling

2. **Study OpenCV:**
   - Video capture: `cv2.VideoCapture()`
   - Image processing: `cv2.cvtColor()`, `cv2.imencode()`

3. **Explore MediaPipe:**
   - Pose detection: `mp.solutions.pose.Pose()`
   - Landmark extraction: `results.pose_landmarks`

4. **Frontend Integration:**
   - HTML templates (`templates/index.html`)
   - CSS styling (`static/css/style.css`)
   - JavaScript interactions (`static/js/main.js`)

### Key Files to Study

- `app.py` - Main application logic
- `models/pose_detector.py` - Pose detection class
- `static/js/main.js` - Frontend behavior
- `templates/index.html` - UI structure

---

## 🎯 Common Issues & Solutions

### MediaPipe Installation Error
**Problem:** `No matching distribution found for mediapipe`
**Solution:** Use Python 3.10 or 3.11:
```powershell
.\setup.ps1 -Python "py -3.10"
```

### Camera Not Detected
**Problem:** `/capture` returns error
**Solution:** 
- Check camera permissions
- Try different camera index: `cv2.VideoCapture(1)`
- Test camera with: `python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"`

### Import Errors in IDE
**Problem:** Red underlines on imports
**Solution:** 
- Select Python interpreter from venv
- VS Code: `Ctrl+Shift+P` → "Python: Select Interpreter"

---

## 🔧 Configuration

### Adjust Pose Detection Confidence

Edit in `app.py`:
```python
pose = mp_pose.Pose(
    min_detection_confidence=0.5,  # 0.0 to 1.0
    min_tracking_confidence=0.5    # 0.0 to 1.0
)
```

### Change Server Port

Edit in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change port here
```

---

## 🚀 Future Enhancements

- [ ] Add voice feedback using pyttsx3
- [ ] Implement pose correction suggestions
- [ ] Add workout session tracking
- [ ] Create pose accuracy scoring
- [ ] Support for multiple users simultaneously
- [ ] Export workout data to PDF/CSV
- [ ] Mobile responsive improvements
- [ ] Add more yoga poses to classification

---

## 📦 Dependencies

- `flask>=2.0` - Web framework
- `opencv-python>=4.5` - Computer vision
- `mediapipe>=0.10` - Pose detection
- `numpy` - Numerical operations
- `pyttsx3` - Text-to-speech (planned feature)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

## 📄 License

This project is created by **TEAM CODEASTRA** for educational purposes.

---

## 🙏 Acknowledgments

- MediaPipe by Google
- OpenCV Community
- Flask Framework
- TEAM CODEASTRA

---

## 📞 Support

For questions or issues, please open an issue on the repository.

**Happy Yoga! 🧘‍♀️🧘‍♂️**
