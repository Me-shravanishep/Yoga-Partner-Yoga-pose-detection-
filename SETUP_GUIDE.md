# 🧘 Yoga Partner - Setup & Run Guide (Error-Free)

## ✅ Prerequisites
- **Python 3.11** installed (NOT 3.13 - MediaPipe compatibility)
- **Windows/Mac/Linux** system
- **Webcam** for pose detection
- **Git** installed

---

## 📝 Step-by-Step Setup Process

### **Step 1: Navigate to Project Directory**
```powershell
cd "c:\Users\YUGANTI\OneDrive\Desktop\Documents\GitHub\Yoga-Partner-Yoga-pose-detection-"
```

### **Step 2: Create Virtual Environment** (If not exists)
```powershell
py -3.11 -m venv venv
```

### **Step 3: Activate Virtual Environment**
```powershell
.\venv\Scripts\Activate.ps1
```
✅ You should see `(venv)` prefix in PowerShell prompt

### **Step 4: Install Dependencies** (DO THIS FIRST - In Order)

**A. Upgrade pip and setuptools:**
```powershell
python -m pip install --upgrade pip setuptools
```

**B. Install core packages:**
```powershell
pip install flask==2.3.0
pip install numpy==1.26.4
pip install opencv-contrib-python==4.8.1.78
pip install mediapipe==0.10.8
pip install protobuf==3.20.3
pip install Pillow==10.0.0
pip install matplotlib==3.7.2
pip install pyttsx3
```

✅ **Do NOT install all at once** - install in this exact order to avoid conflicts

### **Step 5: Verify Installation**
```powershell
python -c "import flask; import cv2; import mediapipe; print('✓ All dependencies OK')"
```

### **Step 6: Run the Application**
```powershell
python app.py
```

### **Step 7: Access in Browser**
Open your web browser and go to:
```
http://127.0.0.1:5000
```

---

## 🎯 What You'll See (No Errors)

✅ **Expected Output:**
```
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
```

---

## 🚨 Common Issues & Fixes

### **Issue 1: "ModuleNotFoundError: No module named 'flask'"**
**Fix:** Ensure venv is activated (you should see `(venv)` in terminal)
```powershell
.\venv\Scripts\Activate.ps1
```

### **Issue 2: "opencv" or "cv2" import error**
**Fix:** Reinstall opencv properly
```powershell
pip uninstall opencv-contrib-python -y
pip install opencv-contrib-python==4.8.1.78
```

### **Issue 3: "mediapipe" import error**
**Fix:** Install in correct order
```powershell
pip uninstall mediapipe protobuf -y
pip install protobuf==3.20.3
pip install mediapipe==0.10.8
```

### **Issue 4: Port 5000 already in use**
**Fix:** Kill existing Flask process
```powershell
Get-Process python | Stop-Process -Force
```
Then restart: `python app.py`

### **Issue 5: "TensorFlow" or "PIL" errors**
**Fix:** Reinstall Pillow
```powershell
pip uninstall Pillow -y
pip install Pillow==10.0.0
```

### **Issue 6: AttributeError or Recursion errors**
**Fix:** Clear cache and reinstall all
```powershell
pip cache purge
pip install -r requirements.txt --force-reinstall
```

---

## 📱 Usage in Browser

1. **Home Page** - Click "Detect Pose" or go to `/page2`
2. **Pose Selection** - Choose a yoga pose (Tree, Butterfly, etc.)
3. **Webcam Stream** - App will show live video with pose detection
4. **Real-time Feedback** - Shows pose score and tips
5. **Dashboard** - Login to view your progress (test account available)

---

## 🔑 Test Credentials

If you see login page:
- **Username:** test
- **Password:** test

Or register a new account using the registration form.

---

## 🛑 To Stop the App

In the terminal, press:
```
CTRL + C
```

---

## ✨ Success Checklist

- [ ] Python 3.11 installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed in order
- [ ] No error messages when importing modules
- [ ] App running on `http://127.0.0.1:5000`
- [ ] Browser shows the yoga detection interface
- [ ] Webcam access granted

---

## 📚 Project Structure

```
Yoga-Partner/
├── app.py                 # Main Flask application
├── requirements.txt       # Dependencies list
├── models/
│   └── pose_detector.py  # Pose detection logic
├── templates/            # HTML pages
├── static/              # CSS, JS, images
├── dataset/             # Training pose images
└── venv/                # Virtual environment
```

---

## 🔧 Troubleshooting Commands

```powershell
# Check Python version
python --version

# Check pip packages
pip list

# Check Flask version
python -c "import flask; print(flask.__version__)"

# Check MediaPipe
python -c "import mediapipe; print('MediaPipe OK')"

# See all errors/warnings
python app.py 2>&1
```

---

## 💡 Tips for Smooth Running

1. **Use PowerShell** (NOT Command Prompt)
2. **Close other apps** using webcam (Zoom, Teams, etc.)
3. **Install packages one-by-one** to catch errors
4. **Don't use Python 3.13** - use 3.11 exactly
5. **Keep requirements versions exact** as listed

---

✅ **If you follow these steps, you'll run the app without errors!**
