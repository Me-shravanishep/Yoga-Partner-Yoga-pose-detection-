# 📊 VISUAL INSTALLATION ROADMAP

```
┌─────────────────────────────────────────────────────────────────────┐
│  CURRENT STATUS: Python 3.13 (MediaPipe NOT Compatible)            │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 1: Download Python 3.11                                       │
│  ─────────────────────────────────────────                          │
│  🌐 Browser opened automatically                                     │
│  📥 Click: "Windows installer (64-bit)"                             │
│  💾 File: python-3.11.10-amd64.exe (~25 MB)                         │
│  ⏱️  Time: 2-3 minutes                                               │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 2: Run Installer                                              │
│  ────────────────────────                                           │
│  1. Double-click python-3.11.10-amd64.exe                           │
│  2. ✅ CHECK: "Add python.exe to PATH"                              │
│  3. Click: "Install Now"                                            │
│  4. Wait for green checkmark                                        │
│  5. Click: "Close"                                                  │
│  ⏱️  Time: 2-3 minutes                                               │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 3: Verify Installation                                        │
│  ──────────────────────────                                         │
│  Open NEW PowerShell:                                               │
│  > py -3.11 --version                                               │
│                                                                      │
│  Expected output:                                                   │
│  Python 3.11.10                                                     │
│  ⏱️  Time: 30 seconds                                                │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 4: Remove Old Environment                                     │
│  ─────────────────────────────                                      │
│  > cd "path\to\Yoga-Partner-Yoga-pose-detection-"                   │
│  > Remove-Item -Recurse -Force venv                                 │
│                                                                      │
│  This deletes the Python 3.13 environment                           │
│  ⏱️  Time: 30 seconds                                                │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 5: Create New Environment (Python 3.11)                       │
│  ────────────────────────────────────────────                       │
│  > py -3.11 -m venv venv                                            │
│  > .\venv\Scripts\Activate.ps1                                      │
│                                                                      │
│  You should see (venv) in prompt                                    │
│  ⏱️  Time: 1 minute                                                  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 6: Install Dependencies                                       │
│  ───────────────────────────                                        │
│  > pip install -r requirements.txt                                  │
│                                                                      │
│  Installs:                                                          │
│  ✅ flask                                                            │
│  ✅ opencv-python                                                    │
│  ✅ mediapipe          ← This will work now!                        │
│  ✅ numpy                                                            │
│  ✅ pyttsx3                                                          │
│  ⏱️  Time: 2-3 minutes (downloads ~200 MB)                           │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 7: Verify MediaPipe                                           │
│  ───────────────────────                                            │
│  > python -c "import mediapipe; print('SUCCESS!')"                  │
│                                                                      │
│  Expected output:                                                   │
│  SUCCESS!                                                           │
│  ⏱️  Time: 10 seconds                                                │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 8: Run Full App                                               │
│  ──────────────────────                                             │
│  > python app.py                                                    │
│                                                                      │
│  Server starts at: http://127.0.0.1:5000                            │
│  ⏱️  Time: 10 seconds                                                │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  🎉 FINAL STATUS: Full Pose Detection Working!                      │
│  ────────────────────────────────────────────────                   │
│  ✅ Python 3.11                                                      │
│  ✅ MediaPipe installed                                              │
│  ✅ Real-time pose detection                                         │
│  ✅ Skeleton overlay on video                                        │
│  ✅ 33 body landmarks tracked                                        │
│  ✅ Yoga pose classification                                         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ⏱️ Total Time Estimate

| Step | Task | Time |
|------|------|------|
| 1 | Download Python 3.11 | 2-3 min |
| 2 | Install Python 3.11 | 2-3 min |
| 3 | Verify installation | 30 sec |
| 4 | Remove old venv | 30 sec |
| 5 | Create new venv | 1 min |
| 6 | Install dependencies | 2-3 min |
| 7 | Verify MediaPipe | 10 sec |
| 8 | Run app | 10 sec |
| **TOTAL** | **Complete setup** | **~10 minutes** |

---

## 🎯 What You're Doing

```
┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│  Python 3.13     │         │  Python 3.11     │         │  Python 3.11     │
│  (Current)       │   →     │  (Install)       │   →     │  + MediaPipe     │
│                  │         │                  │         │  (Working!)      │
│  ✅ Flask         │         │  ✅ Flask         │         │  ✅ Flask         │
│  ✅ OpenCV        │         │  ✅ OpenCV        │         │  ✅ OpenCV        │
│  ❌ MediaPipe     │         │  ✅ MediaPipe     │         │  ✅ MediaPipe     │
│  ✅ NumPy         │         │  ✅ NumPy         │         │  ✅ NumPy         │
└──────────────────┘         └──────────────────┘         └──────────────────┘
   Demo version              After installation           Full pose detection
   (No skeleton)                                          (Skeleton overlay)
```

---

## 📋 Quick Reference Card

```
╔═══════════════════════════════════════════════════════════════╗
║  BEFORE YOU START                                             ║
╠═══════════════════════════════════════════════════════════════╣
║  1. Browser tab with Python download should be open           ║
║  2. Stop current Flask server (Ctrl+C)                        ║
║  3. Have project path ready to copy                           ║
╚═══════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════╗
║  COPY-PASTE COMMANDS (After Python 3.11 installed)           ║
╠═══════════════════════════════════════════════════════════════╣
║  cd "c:\Users\shrav\OneDrive\Desktop\YOGA POSE DETECTION\    ║
║  Yoga-Partner-Yoga-pose-detection-"                           ║
║                                                               ║
║  Remove-Item -Recurse -Force venv                             ║
║  py -3.11 -m venv venv                                        ║
║  .\venv\Scripts\Activate.ps1                                  ║
║  pip install -r requirements.txt                              ║
║  python app.py                                                ║
╚═══════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════╗
║  SUCCESS INDICATORS                                           ║
╠═══════════════════════════════════════════════════════════════╣
║  ✓ py -3.11 --version → Shows "Python 3.11.10"               ║
║  ✓ (venv) appears in PowerShell prompt                        ║
║  ✓ pip install completes without errors                       ║
║  ✓ import mediapipe → No error                                ║
║  ✓ python app.py → Server starts                              ║
║  ✓ Browser shows skeleton overlay on video                    ║
╚═══════════════════════════════════════════════════════════════╝
```

---

**🎯 YOUR CURRENT TASK: Download and install Python 3.11 from the opened browser tab!**
