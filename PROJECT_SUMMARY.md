# ✅ Project Setup Complete!

## 📦 What Has Been Created

Your Yoga Pose Detection project now has a **complete Flask-based structure**:

### ✅ Core Application Files
- ✅ `app.py` - Main Flask backend with 6 routes
- ✅ `requirements.txt` - All dependencies (Flask, OpenCV, MediaPipe, NumPy, pyttsx3)
- ✅ `setup.ps1` - Windows PowerShell setup script

### ✅ Frontend Files
- ✅ `templates/index.html` - Main HTML page with video feed and user registration
- ✅ `static/css/style.css` - Professional styling with gradient background
- ✅ `static/js/main.js` - JavaScript for video control and API calls

### ✅ Backend Logic
- ✅ `models/pose_detector.py` - Complete PoseDetector class with:
  - Pose detection using MediaPipe
  - Landmark extraction
  - Angle calculation
  - Basic pose classification
  - Reference data for 6 yoga poses
- ✅ `models/__init__.py` - Python package initialization
- ✅ `models/README.md` - Documentation for the pose detector

### ✅ Data Storage
- ✅ `data/` folder - For storing user JSON records
- ✅ `data/sample_data.json` - Example data structure

### ✅ Static Assets Folders
- ✅ `static/css/` - For stylesheets
- ✅ `static/js/` - For JavaScript files
- ✅ `static/images/` - For image assets
- ✅ `static/uploads/` - For uploaded files

### ✅ Documentation
- ✅ `PROJECT_README.md` - Comprehensive documentation
- ✅ `QUICKSTART.md` - Step-by-step setup guide
- ✅ `.gitignore` - Properly configured for Python/Flask projects

---

## 🎯 What the App Does

### Routes (Endpoints):
1. **GET /** - Main landing page with video feed and user form
2. **GET /health** - Health check and library versions
3. **GET /capture** - Single frame camera test
4. **GET /video_feed** - MJPEG stream with real-time pose detection
5. **POST /api/save_user** - Save user data to JSON file
6. **GET /api/get_users** - Retrieve all saved users

### Features:
- ✅ Real-time pose landmark detection (33 body points)
- ✅ Visual overlay of skeleton on video
- ✅ User registration form
- ✅ Data persistence (JSON files)
- ✅ Responsive UI with gradient design
- ✅ Health monitoring
- ✅ Keyboard shortcuts (S = start, X = stop)

---

## 🚀 Next Steps - How to Run

### Step 1: Install Dependencies

You need to activate your venv and install packages:

```powershell
cd "c:\Users\shrav\OneDrive\Desktop\YOGA POSE DETECTION\Yoga-Partner-Yoga-pose-detection-"

# If venv exists, activate it
.\venv\Scripts\Activate.ps1

# Install/reinstall all dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Important:** Use Python 3.10 or 3.11 for best MediaPipe compatibility!

### Step 2: Run the Application

```powershell
python app.py
```

### Step 3: Open in Browser

Navigate to: http://127.0.0.1:5000/

---

## 📊 Project Structure Overview

```
Yoga-Partner-Yoga-pose-detection-/
│
├── 📄 app.py                    # Flask backend (120+ lines)
├── 📄 requirements.txt           # Dependencies
├── 📄 setup.ps1                 # Setup automation
│
├── 📁 static/                   # Frontend assets
│   ├── 📁 css/
│   │   └── style.css           # Styles (300+ lines)
│   ├── 📁 js/
│   │   └── main.js             # Frontend logic (100+ lines)
│   ├── 📁 images/              # Image assets
│   └── 📁 uploads/             # User uploads
│
├── 📁 templates/                # HTML templates
│   └── index.html              # Main page (60+ lines)
│
├── 📁 models/                   # Pose detection
│   ├── pose_detector.py        # Core logic (200+ lines)
│   ├── __init__.py             # Package init
│   └── README.md               # Model docs
│
├── 📁 data/                     # User data
│   └── sample_data.json        # Example structure
│
├── 📁 venv/                     # Virtual environment
│
├── 📄 PROJECT_README.md         # Full documentation
├── 📄 QUICKSTART.md             # Quick start guide
├── 📄 README.md                 # Original readme
└── 📄 .gitignore               # Git ignore rules
```

---

## 🧠 Learning Path

### Beginner → Intermediate → Advanced

**Week 1: Understand the Stack**
- Study Flask routing in `app.py`
- Learn how templates work (`index.html`)
- Understand static file serving

**Week 2: OpenCV Basics**
- How video capture works: `cv2.VideoCapture()`
- Image encoding: `cv2.imencode()`
- Color space conversion: `cv2.cvtColor()`

**Week 3: MediaPipe Deep Dive**
- Read MediaPipe documentation
- Study `pose_detector.py` line by line
- Experiment with different confidence values

**Week 4: Extend the App**
- Add new yoga poses
- Implement pose accuracy scoring
- Add voice feedback using pyttsx3

---

## 🎓 Key Concepts to Learn

### 1. Flask Framework
- **Routing**: `@app.route()` decorators
- **Templates**: Jinja2 templating engine
- **Static files**: `url_for('static', filename='...')`
- **JSON APIs**: `jsonify()` function
- **Request handling**: `request.json`

### 2. OpenCV (cv2)
- **Video capture**: Getting frames from camera
- **Image processing**: Color conversions, encoding
- **MJPEG streaming**: Yielding frames in Response

### 3. MediaPipe
- **Pose estimation**: 33 body landmarks
- **Landmark coordinates**: Normalized x, y, z values
- **Drawing utilities**: Visual overlay
- **Confidence thresholds**: Detection vs tracking

### 4. Frontend Integration
- **Fetch API**: Making HTTP requests from JavaScript
- **Event handling**: Button clicks, form submission
- **DOM manipulation**: Updating page content
- **Image streaming**: Displaying MJPEG in `<img>` tag

---

## 💡 Code Examples from Your Project

### Example 1: How Pose Detection Works

```python
# From app.py - video_feed route
image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert for MediaPipe
results = pose.process(image)                    # Detect pose
if results.pose_landmarks:
    mp_drawing.draw_landmarks(...)               # Draw skeleton
```

### Example 2: How Angles are Calculated

```python
# From pose_detector.py
def calculate_angle(self, point1, point2, point3):
    # Uses arctangent to find angle between three points
    radians = np.arctan2(y3-y2, x3-x2) - np.arctan2(y1-y2, x1-x2)
    angle = np.abs(radians * 180.0 / np.pi)
```

### Example 3: How User Data is Saved

```python
# From app.py - save_user route
user_data['timestamp'] = datetime.now().isoformat()
filename = f"data/user_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(filename, 'w') as f:
    json.dump(user_data, f, indent=2)
```

---

## 🔧 Customization Ideas

### Easy Customizations:
1. Change colors in `style.css`
2. Add your team logo to `static/images/`
3. Modify confidence thresholds in `app.py`

### Medium Customizations:
1. Add more yoga poses to `pose_detector.py`
2. Create a pose history/statistics page
3. Add export functionality (CSV/PDF)

### Advanced Customizations:
1. Train ML model for better pose classification
2. Add multi-user support with database
3. Implement real-time pose correction feedback
4. Add voice coaching using pyttsx3

---

## 📚 Resources to Learn More

- **Flask Tutorial**: https://flask.palletsprojects.com/tutorial/
- **OpenCV Python**: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
- **MediaPipe Pose**: https://google.github.io/mediapipe/solutions/pose.html
- **JavaScript Fetch API**: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

---

## ✅ Checklist Before Running

- [ ] Python 3.10 or 3.11 installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Webcam available and not in use by other apps
- [ ] Windows camera permissions enabled

---

## 🎉 You're Ready!

Your complete Flask-based Yoga Pose Detection project is set up!

**Total Lines of Code:** ~800+ lines across all files
**Technologies:** Flask, OpenCV, MediaPipe, JavaScript, HTML/CSS
**Features:** Real-time pose detection, user management, REST API

**Start learning by:**
1. Reading through `QUICKSTART.md`
2. Installing dependencies
3. Running `python app.py`
4. Exploring each file to understand how it works

**TEAM CODEASTRA - Happy Coding! 🧘‍♀️💻**
