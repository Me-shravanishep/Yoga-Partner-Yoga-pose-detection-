# 🎯 SIMPLE 3-STEP GUIDE TO GET MEDIAPIPE WORKING

## Step 1️⃣: Download & Install Python 3.11 (5 minutes)

### Download:
🔗 Browser should be open with download page
OR visit: https://www.python.org/ftp/python/3.11.10/python-3.11.10-amd64.exe

### Install:
1. Double-click the downloaded file
2. ✅ CHECK: "Add python.exe to PATH" 
3. Click "Install Now"
4. Wait for completion
5. Close installer

---

## Step 2️⃣: Recreate Virtual Environment (2 minutes)

Open a **NEW** PowerShell and copy-paste this:

```powershell
cd "c:\Users\shrav\OneDrive\Desktop\YOGA POSE DETECTION\Yoga-Partner-Yoga-pose-detection-"
Remove-Item -Recurse -Force venv
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
pip install flask opencv-python mediapipe numpy pyttsx3
```

---

## Step 3️⃣: Run the Full App (30 seconds)

```powershell
python app.py
```

Open browser: http://127.0.0.1:5000

Click "Start Detection" → See skeleton on your body! 🎉

---

## ✅ Expected Result:

When you click "Start Detection":
- Your webcam opens
- Blue and pink skeleton appears on your body
- 33 points track your movements
- Real-time pose detection works!

---

## 🆘 If Something Goes Wrong:

### Can't find py -3.11?
- Restart PowerShell after installing Python 3.11
- Or use full path: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe`

### MediaPipe fails to install?
```powershell
pip install mediapipe==0.10.9
```

### Port 5000 in use?
Stop the current server (Ctrl+C) first

---

**That's it! Just 3 steps to full pose detection! 🧘‍♀️**
