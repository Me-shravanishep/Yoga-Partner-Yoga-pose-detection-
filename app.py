 
from flask import Flask, render_template, Response, jsonify, request
import cv2
import mediapipe as mp
import numpy as np
import json
import os
from datetime import datetime
import tempfile
import urllib.request
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = 'yoga_secret_key_2025'  # Change this in production

# --- User Auth Helpers ---
import hashlib
USERS_FILE = 'users.json'
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r') as f:
        data = json.load(f)
        return data.get('users', [])
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump({'users': users}, f, indent=2)
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# --- Auth Routes ---
from flask import redirect, url_for, session
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        user = next((u for u in users if u['username'] == username and u['password'] == hash_pw(password)), None)
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if any(u['username'] == username for u in users):
            return render_template('register.html', error='Username already exists')
        users.append({'username': username, 'password': hash_pw(password), 'history': []})
        save_users(users)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Configure upload folder and data folder
UPLOAD_FOLDER = 'static/uploads'
DATA_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')


@app.route('/analyze')
def analyze_page():
    """Render analyze page for video URL input"""
    return render_template('analyze.html')


@app.route('/health')
def health():
    """Health check endpoint - returns versions of installed libraries"""
    versions = {
        'opencv': cv2.__version__,
        'mediapipe': getattr(mp, '__version__', 'unknown'),
        'numpy': np.__version__,
    }
    return jsonify({'status': 'ok', 'versions': versions})


@app.route('/capture')
def capture_once():
    """Capture a single frame from default camera and return its size as a quick test"""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return jsonify({'error': 'cannot open camera'}), 500
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return jsonify({'error': 'failed to read frame'}), 500
    h, w = frame.shape[:2]
    return jsonify({'width': w, 'height': h})


@app.route('/video_feed')
def video_feed():
    """Video streaming route - returns MJPEG stream"""
    def generate():
        cap = cv2.VideoCapture(0)
        while True:
            success, frame = cap.read()
            if not success:
                break
            
            # Convert BGR to RGB for MediaPipe
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # Process with MediaPipe Pose
            results = pose.process(image)
            
            # Convert back to BGR for OpenCV
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Draw pose landmarks if detected
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                )
            
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        cap.release()
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


def _download_video_to_temp(url: str) -> str:
    """Download a remote video to a temporary file and return the path."""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    parsed = urlparse(url)
    ext = os.path.splitext(parsed.path)[1] or '.mp4'
    fd, tmp_path = tempfile.mkstemp(prefix='vid_', suffix=ext, dir=UPLOAD_FOLDER)
    os.close(fd)
    urllib.request.urlretrieve(url, tmp_path)
    return tmp_path


def _evaluate_pose_correctness(pose_name: str, landmarks: list) -> dict:
    """Very simple heuristic correctness scorer by pose; placeholder for ML model."""
    score = 0.0
    tips = []
    if not landmarks or len(landmarks) < 33:
        return { 'score': 0.0, 'tips': ['No pose detected'] }

    # Example heuristics: straight legs/arms for mountain/plank, knee angle for warrior
    def angle(a,b,c):
        ax,ay = landmarks[a].x, landmarks[a].y
        bx,by = landmarks[b].x, landmarks[b].y
        cx,cy = landmarks[c].x, landmarks[c].y
        v1 = np.array([ax-bx, ay-by]); v2 = np.array([cx-bx, cy-by])
        cosang = np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)+1e-6)
        ang = np.degrees(np.arccos(np.clip(cosang,-1,1)))
        return ang

    try:
        if pose_name in ['mountain','plank']:
            lk = angle(23,25,27)  # left hip-knee-ankle
            rk = angle(24,26,28)
            la = angle(11,13,15)  # left shoulder-elbow-wrist
            ra = angle(12,14,16)
            # Closer to 180 is better
            legs = (360 - abs(180-lk) - abs(180-rk)) / 360
            arms = (360 - abs(180-la) - abs(180-ra)) / 360
            score = max(0.0, min(1.0, 0.5*legs + 0.5*arms))
            if lk < 165 or rk < 165: tips.append('Straighten legs more')
            if la < 165 or ra < 165: tips.append('Straighten arms more')
        elif pose_name.startswith('warrior'):
            fwd = angle(23,25,27)  # sample: check left knee bend
            score = max(0.0, min(1.0, 1 - abs(90 - fwd)/90))
            if fwd > 120: tips.append('Bend front knee closer to 90°')
            if fwd < 60: tips.append('Avoid over-bending the knee')
        elif pose_name == 'tree':
            # Use ankle y-difference as a crude balance check (placeholder)
            score = 0.6
            tips.append('Keep core engaged and steady')
        else:
            score = 0.5
            tips.append('Pose heuristic not defined, using default score')
    except Exception:
        return { 'score': 0.0, 'tips': ['Error evaluating pose'] }

    return { 'score': float(round(score, 3)), 'tips': tips }


@app.route('/api/analyze_video', methods=['POST'])
def api_analyze_video():
    """Analyze a remote/local video for pose correctness against a target pose."""
    data = request.get_json(force=True)
    url = data.get('url')
    target_pose = (data.get('target_pose') or 'mountain').lower()
    if not url:
        return jsonify({'status':'error','message':'Missing video url'}), 400

    # Try to open URL directly with OpenCV first; if it fails, download to temp
    cap = cv2.VideoCapture(url)
    temp_path = None
    if not cap.isOpened():
        try:
            temp_path = _download_video_to_temp(url)
            cap = cv2.VideoCapture(temp_path)
        except Exception as e:
            return jsonify({'status':'error','message':f'Cannot open video: {e}'}), 400

    total_frames = 0
    analyzed_frames = 0
    max_frames = 300  # limit work for long videos (~10s at 30fps)
    pose_scores = []

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as analyzer:
        while total_frames < max_frames:
            ok, frame = cap.read()
            if not ok:
                break
            total_frames += 1
            # Downscale for speed
            h,w = frame.shape[:2]
            scale = 640 / max(1,w)
            if scale < 1:
                frame = cv2.resize(frame, (int(w*scale), int(h*scale)))

            # Run mediapipe
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb.flags.writeable = False
            res = analyzer.process(rgb)
            if not res.pose_landmarks:
                continue
            analyzed_frames += 1
            eval_res = _evaluate_pose_correctness(target_pose, res.pose_landmarks.landmark)
            pose_scores.append(eval_res['score'])

    cap.release()
    if temp_path and os.path.exists(temp_path):
        try: os.remove(temp_path)
        except Exception: pass

    if analyzed_frames == 0:
        return jsonify({'status':'ok','frames':total_frames,'analyzed':0,'message':'No pose detected in video'}), 200

    avg_score = float(round(sum(pose_scores)/len(pose_scores), 3))
    verdict = 'correct' if avg_score >= 0.7 else ('almost' if avg_score >= 0.5 else 'incorrect')
    return jsonify({
        'status':'ok',
        'frames': total_frames,
        'analyzed': analyzed_frames,
        'target_pose': target_pose,
        'average_score': avg_score,
        'verdict': verdict
    })


@app.route('/api/save_user', methods=['POST'])
def save_user():
    """Save user data to JSON file"""
    try:
        user_data = request.json
        user_data['timestamp'] = datetime.now().isoformat()
        
        # Save to data folder
        filename = f"{DATA_FOLDER}/user_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        return jsonify({'status': 'success', 'message': 'User data saved', 'file': filename})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/get_users')
def get_users():
    """Retrieve all saved user data"""
    try:
        users = []
        for filename in os.listdir(DATA_FOLDER):
            if filename.endswith('.json'):
                with open(os.path.join(DATA_FOLDER, filename), 'r') as f:
                    users.append(json.load(f))
        return jsonify({'status': 'success', 'users': users})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
