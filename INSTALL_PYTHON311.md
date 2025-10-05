# 📥 Installing Python 3.11 for MediaPipe Support

## 🎯 Quick Installation Steps

### Step 1: Download Python 3.11

The download page should have opened in your browser. If not, visit:
**https://www.python.org/downloads/release/python-31110/**

**For Windows 64-bit (recommended):**
Scroll down and download: **Windows installer (64-bit)**

Direct link: https://www.python.org/ftp/python/3.11.10/python-3.11.10-amd64.exe

### Step 2: Run the Installer

1. **Double-click** the downloaded `.exe` file
2. ⚠️ **IMPORTANT:** Check these boxes:
   - ✅ **"Add python.exe to PATH"** (at the bottom)
   - ✅ **"Install for all users"** (optional but recommended)
3. Click **"Install Now"** (recommended) or **"Customize installation"** (advanced)

### Step 3: Verify Installation

After installation completes, open a **NEW PowerShell window** and run:

```powershell
py -3.11 --version
```

You should see: `Python 3.11.10` (or similar)

---

## 🔧 After Python 3.11 is Installed

### Option A: Automatic Setup (Run One Command)

```powershell
# Navigate to your project
cd "c:\Users\shrav\OneDrive\Desktop\YOGA POSE DETECTION\Yoga-Partner-Yoga-pose-detection-"

# Run the setup script (this will recreate venv with Python 3.11)
.\setup.ps1 -Python "py -3.11"
```

### Option B: Manual Setup (Step by Step)

```powershell
# 1. Navigate to project directory
cd "c:\Users\shrav\OneDrive\Desktop\YOGA POSE DETECTION\Yoga-Partner-Yoga-pose-detection-"

# 2. Remove old virtual environment (Python 3.13)
Remove-Item -Recurse -Force venv

# 3. Create new virtual environment with Python 3.11
py -3.11 -m venv venv

# 4. Activate the virtual environment
.\venv\Scripts\Activate.ps1

# 5. Upgrade pip
python -m pip install --upgrade pip

# 6. Install ALL dependencies (including MediaPipe)
pip install -r requirements.txt

# 7. Verify MediaPipe is installed
python -c "import mediapipe; print('MediaPipe version:', mediapipe.__version__)"
```

---

## 🚀 Running the Full App with MediaPipe

After Python 3.11 setup is complete:

```powershell
# Make sure venv is activated
.\venv\Scripts\Activate.ps1

# Run the FULL app (with MediaPipe pose detection)
python app.py
```

Then open: http://127.0.0.1:5000

You should now see:
- ✅ Real-time pose detection
- ✅ Skeleton overlay on video
- ✅ 33 body landmarks tracked
- ✅ Pose classification

---

## 🐛 Troubleshooting

### Problem: "py -3.11 not recognized"

**Solution:** Python 3.11 wasn't added to PATH during installation.

**Fix:**
1. Uninstall Python 3.11 (Windows Settings → Apps)
2. Reinstall and **CHECK** "Add python.exe to PATH"
3. Restart PowerShell

### Problem: "Cannot find Python 3.11"

**Solution:** Find the exact installation path.

```powershell
# Check all installed Python versions
py -0

# If you see Python 3.11 listed, use it:
py -3.11 --version
```

### Problem: MediaPipe still fails to install

**Try installing specific version:**
```powershell
pip install mediapipe==0.10.9
```

### Problem: Execution Policy Error when activating venv

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📋 Installation Checklist

Before proceeding, make sure:
- [ ] Downloaded Python 3.11.10 installer
- [ ] Ran installer with "Add to PATH" checked
- [ ] Verified installation: `py -3.11 --version`
- [ ] Opened NEW PowerShell window (to refresh PATH)
- [ ] Navigated to project directory
- [ ] Removed old venv: `Remove-Item -Recurse -Force venv`
- [ ] Created new venv: `py -3.11 -m venv venv`
- [ ] Activated venv: `.\venv\Scripts\Activate.ps1`
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Verified MediaPipe: `python -c "import mediapipe; print('OK')"`
- [ ] Run full app: `python app.py`

---

## ⚡ Quick Copy-Paste Script

After Python 3.11 is installed, copy and paste this entire block:

```powershell
cd "c:\Users\shrav\OneDrive\Desktop\YOGA POSE DETECTION\Yoga-Partner-Yoga-pose-detection-"
Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -c "import cv2, mediapipe, numpy, flask; print('All libraries installed!'); print('OpenCV:', cv2.__version__); print('MediaPipe:', mediapipe.__version__); print('NumPy:', numpy.__version__); print('Flask:', flask.__version__)"
```

If all imports succeed, run:
```powershell
python app.py
```

---

## 🎯 What Changes After Installing Python 3.11?

### Before (Python 3.13):
- ❌ MediaPipe: Not available
- ✅ Camera feed: Basic video only
- ❌ Pose detection: Disabled
- ❌ Skeleton overlay: None

### After (Python 3.11):
- ✅ MediaPipe: Fully working
- ✅ Camera feed: With pose overlay
- ✅ Pose detection: 33 landmarks tracked
- ✅ Skeleton overlay: Real-time drawing
- ✅ Pose classification: Yoga pose recognition
- ✅ Angle calculation: Joint angles computed

---

## 📞 Need Help?

If you encounter issues:

1. **Check Python version:**
   ```powershell
   py -0  # Lists all installed Python versions
   ```

2. **Verify venv Python version:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   python --version  # Should show Python 3.11.x
   ```

3. **Test MediaPipe installation:**
   ```powershell
   pip list | Select-String mediapipe
   ```

4. **Read error logs** and share them if stuck

---

## 🎉 Success Indicators

You'll know everything is working when:

1. ✅ `py -3.11 --version` shows Python 3.11.10
2. ✅ `pip install -r requirements.txt` completes without errors
3. ✅ `import mediapipe` doesn't raise an error
4. ✅ `python app.py` starts without import errors
5. ✅ Opening http://127.0.0.1:5000 shows pose detection working
6. ✅ Camera feed shows skeleton overlay on your body

---

**Download Python 3.11 now from the opened browser tab!**
**Then follow the steps above to complete the setup! 🚀**
