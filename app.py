 
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
from copy import deepcopy

# Shared in-memory feedback for live scoring
LATEST_FEEDBACK = {
    'pose': 'none',
    'score': 0.0,
    'tips': ['Waiting for camera'],
    'verdict': 'not_started',
    'timestamp': None
}

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

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session.get('username', 'User')
    users = load_users()
    user = next((u for u in users if u['username'] == username), None)
    
    if not user:
        return redirect(url_for('login'))
    
    # Initialize ALL default values to ensure no Undefined objects
    weekly_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    weekly_scores = [0, 0, 0, 0, 0, 0, 0]
    pose_labels = []
    pose_distribution = []
    top_poses = []
    recent_sessions = []
    stats = {
        'total_sessions': 0,
        'today_sessions': 0,
        'avg_score': 0,
        'best_score': 0,
        'total_minutes': 0
    }
    
    try:
        # Get user's history and calculate statistics
        history = user.get('history', [])
        
        if not history:
            # Return early with empty data if no history
            return render_template('dashboard.html', 
                                 username=username, 
                                 stats=stats,
                                 weekly_labels=weekly_labels,
                                 weekly_scores=weekly_scores,
                                 pose_labels=pose_labels,
                                 pose_distribution=pose_distribution,
                                 top_poses=top_poses,
                                 recent_sessions=recent_sessions)
        
        # Calculate daily progress
        today = datetime.now().strftime('%Y-%m-%d')
        today_sessions = [h for h in history if h.get('date', '').startswith(today)]
        
        # Calculate weekly progress (last 7 days)
        from datetime import timedelta
        weekly_labels = []
        weekly_scores = []
        
        for i in range(6, -1, -1):  # 7 days, most recent last
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            day_name = (datetime.now() - timedelta(days=i)).strftime('%a')
            day_sessions = [h for h in history if h.get('date', '').startswith(date)]
            
            weekly_labels.append(day_name)
            avg_score = round(sum([s.get('score', 0) for s in day_sessions]) / len(day_sessions) * 100, 1) if day_sessions else 0
            weekly_scores.append(avg_score)
        
        # Calculate pose statistics
        pose_stats = {}
        for entry in history:
            pose = str(entry.get('pose', 'Unknown'))
            if pose not in pose_stats:
                pose_stats[pose] = {'count': 0, 'scores': [], 'best_score': 0}
            pose_stats[pose]['count'] += 1
            score = float(entry.get('score', 0))
            pose_stats[pose]['scores'].append(score)
            pose_stats[pose]['best_score'] = max(pose_stats[pose]['best_score'], score)
        
        # Prepare top poses data
        top_poses = []
        for pose, data in sorted(pose_stats.items(), key=lambda x: x[1]['count'], reverse=True)[:5]:
            avg_score = round(sum(data['scores']) / len(data['scores']) * 100, 1) if data['scores'] else 0
            progress = round((data['scores'][-1] - data['scores'][0]) * 100, 1) if len(data['scores']) > 1 else 0
            top_poses.append({
                'name': str(pose),
                'sessions': int(data['count']),
                'avg_score': float(avg_score),
                'best_score': float(round(data['best_score'] * 100, 1)),
                'progress': float(progress)
            })
        
        # Prepare pose distribution for pie chart
        pose_labels = []
        pose_distribution = []
        for pose, data in sorted(pose_stats.items(), key=lambda x: x[1]['count'], reverse=True)[:6]:
            pose_labels.append(str(pose))
            pose_distribution.append(int(data['count']))
        
        # Recent sessions (last 5)
        recent_sessions = []
        for entry in history[-5:][::-1]:  # Last 5, newest first
            duration_seconds = int(entry.get('duration', 0))
            recent_sessions.append({
                'date': str(entry.get('date', 'Unknown')),
                'pose': str(entry.get('pose', 'Unknown')),
                'score': float(round(entry.get('score', 0) * 100, 1)),
                'duration': f"{duration_seconds // 60}m {duration_seconds % 60}s"
            })
        
        # Calculate total minutes
        total_minutes = sum([int(h.get('duration', 0)) for h in history]) // 60
        
        # Build stats dictionary with proper types
        stats = {
            'total_sessions': int(len(history)),
            'today_sessions': int(len(today_sessions)),
            'avg_score': float(round(sum([h.get('score', 0) for h in history]) / len(history) * 100, 1)) if history else 0.0,
            'best_score': float(round(max([h.get('score', 0) for h in history], default=0) * 100, 1)),
            'total_minutes': int(total_minutes)
        }
        
    except Exception as e:
        print(f"Error calculating dashboard stats: {e}")
        import traceback
        traceback.print_exc()
        # Use the default values already initialized
    
    return render_template('dashboard.html', 
                         username=str(username), 
                         stats=stats,
                         weekly_labels=weekly_labels,
                         weekly_scores=weekly_scores,
                         pose_labels=pose_labels,
                         pose_distribution=pose_distribution,
                         top_poses=top_poses,
                         recent_sessions=recent_sessions)

@app.route('/page2')

@app.route('/page2')
def page2():
    return render_template('page2.html')

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
    """Video streaming route - returns MJPEG stream with live scoring overlay."""
    target_pose = _normalize_pose_slug(request.args.get('pose_slug', 'tree'))

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

            feedback = {'score': 0.0, 'tips': ['No pose detected']}

            # Draw pose landmarks if detected with wireframe-style colored borders
            if results.pose_landmarks:
                # Custom drawing specs for AR wireframe look - thin colored lines, no fill
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=1, circle_radius=3),  # Cyan dots
                    mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=1)   # Cyan lines
                )
                feedback = _evaluate_pose_correctness(target_pose, results.pose_landmarks.landmark)

            verdict = 'incorrect'
            if feedback['score'] >= 0.7:
                verdict = 'correct'
            elif feedback['score'] >= 0.5:
                verdict = 'almost'

            # Add text overlays without background
            h, w = image.shape[:2]
            font = cv2.FONT_HERSHEY_SIMPLEX
            
            # Right-aligned percentage in white - with safe margin from close button
            percentage_text = f"{feedback['score']*100:.0f}%"
            text_size = cv2.getTextSize(percentage_text, font, 1.2, 2)[0]
            text_x = w - text_size[0] - 100
            if text_x < 20:
                text_x = 20
            cv2.putText(image, percentage_text, (text_x, 48), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Bottom instruction text
            tip_text = feedback['tips'][0] if feedback.get('tips') else ''
            if tip_text and len(tip_text) > 0:
                tip_size = cv2.getTextSize(tip_text[:50], font, 0.6, 2)[0]
                tip_x = (w - tip_size[0]) // 2
                cv2.putText(image, tip_text[:50], (tip_x, h - 25), font, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

            # Update shared feedback for polling API
            LATEST_FEEDBACK.update({
                'pose': target_pose,
                'score': float(round(feedback['score'], 3)),
                'tips': feedback.get('tips', []),
                'verdict': verdict,
                'timestamp': datetime.utcnow().isoformat()
            })

            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', image)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

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


def _normalize_pose_slug(name: str) -> str:
    """Normalize pose names to compact slugs used across the API."""
    if not name:
        return 'tree'
    raw = name.lower()
    replacements = {
        'vrikshasana': 'tree',
        'tree': 'tree',
        'butterfly': 'butterfly',
        'baddha': 'butterfly',
        'konasana': 'butterfly',
        'cobra': 'cobra',
        'bhujangasana': 'cobra',
        'downward': 'downdog',
        'adho': 'downdog',
        'dog': 'downdog',
        'balasana': 'child',
        "child's": 'child',
        'child': 'child',
        'cat-cow': 'catcow',
        'cat cow': 'catcow',
        'cat': 'catcow',
        'cow': 'catcow',
        'marjaryasana': 'catcow',
        'bitilasana': 'catcow'
    }
    for key, val in replacements.items():
        if key in raw:
            return val
    return raw.replace(' ', '-')


def _evaluate_pose_correctness(pose_name: str, landmarks: list) -> dict:
    """Very simple heuristic correctness scorer by pose; placeholder for ML model."""
    score = 0.0
    tips = []
    if not landmarks or len(landmarks) < 33:
        return { 'score': 0.0, 'tips': ['No pose detected'] }

    pose_slug = _normalize_pose_slug(pose_name)

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
        if pose_slug in ['mountain','plank']:
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
        elif pose_slug.startswith('warrior'):
            fwd = angle(23,25,27)  # sample: check left knee bend
            score = max(0.0, min(1.0, 1 - abs(90 - fwd)/90))
            if fwd > 120: tips.append('Bend front knee closer to 90°')
            if fwd < 60: tips.append('Avoid over-bending the knee')
        elif pose_slug == 'tree':
            left_ankle_y = landmarks[27].y
            right_ankle_y = landmarks[28].y
            ankle_gap = abs(left_ankle_y - right_ankle_y)
            hand_height = (landmarks[15].y + landmarks[16].y) / 2
            head_height = landmarks[0].y
            arms_up = max(0.0, min(1.0, (head_height - hand_height + 0.25)))
            score = max(0.0, min(1.0, 0.7 * min(1.0, ankle_gap * 3) + 0.3 * arms_up))
            if ankle_gap < 0.05: tips.append('Lift one foot to the inner thigh')
            if arms_up < 0.5: tips.append('Reach both arms overhead for stability')
        elif pose_slug == 'butterfly':
            left_knee_angle = angle(23,25,27)
            right_knee_angle = angle(24,26,28)
            hip_open = (360 - abs(140-left_knee_angle) - abs(140-right_knee_angle)) / 360
            score = max(0.0, min(1.0, hip_open))
            if left_knee_angle > 160 or right_knee_angle > 160:
                tips.append('Bring feet closer to pelvis, let knees drop outward')
            tips.append('Keep spine long; avoid rounding forward')
        elif pose_slug == 'cobra':
            spine_angle = angle(11,23,25)
            elbow_angle = angle(11,13,15)
            lift_score = max(0.0, min(1.0, (spine_angle-120)/80))
            arms_score = max(0.0, min(1.0, (elbow_angle-70)/110))
            score = max(0.0, min(1.0, 0.6*lift_score + 0.4*arms_score))
            if spine_angle < 150: tips.append('Lift the chest forward and up without crunching the lower back')
            if elbow_angle < 120: tips.append('Soften elbows under shoulders, avoid locking arms')
        elif pose_slug == 'downdog':
            hip_angle = angle(11,23,25)
            knee_angle_l = angle(23,25,27)
            knee_angle_r = angle(24,26,28)
            shoulder_angle = angle(11,23,31) if len(landmarks) > 31 else hip_angle
            hip_score = max(0.0, min(1.0, (110 - abs(90-hip_angle)) / 110))
            leg_score = max(0.0, min(1.0, (360 - abs(175-knee_angle_l) - abs(175-knee_angle_r)) / 360))
            shoulder_score = max(0.0, min(1.0, (180 - abs(160-shoulder_angle)) / 180))
            score = max(0.0, min(1.0, 0.4*hip_score + 0.4*leg_score + 0.2*shoulder_score))
            if knee_angle_l < 160 or knee_angle_r < 160:
                tips.append('Try straightening the legs; pedal the feet if hamstrings are tight')
            tips.append('Press the mat away and lift hips high to form an inverted V')
        elif pose_slug == 'child':
            hip_fold = angle(11,23,25)
            knee_bend = angle(23,25,27)
            arm_extension = angle(11,13,15)
            fold_score = max(0.0, min(1.0, (170 - hip_fold)/170))
            knee_score = max(0.0, min(1.0, (150 - abs(120-knee_bend))/150))
            arm_score = max(0.0, min(1.0, (180 - abs(165-arm_extension))/180))
            score = max(0.0, min(1.0, 0.5*fold_score + 0.3*knee_score + 0.2*arm_score))
            tips.append('Sink hips toward heels and reach arms forward for a gentle stretch')
        elif pose_slug == 'catcow':
            hip_angle = angle(11,23,25)
            knee_angle = angle(23,25,27)
            spine_roundness = abs(landmarks[0].z - landmarks[23].z)
            hip_score = max(0.0, min(1.0, (120 - abs(100-hip_angle)) / 120))
            knee_score = max(0.0, min(1.0, (120 - abs(100-knee_angle)) / 120))
            spine_score = max(0.0, min(1.0, 1 - min(0.7, spine_roundness)))
            score = max(0.0, min(1.0, 0.4*hip_score + 0.4*knee_score + 0.2*spine_score))
            tips.append('Move slowly between cat (round) and cow (arch) while keeping knees under hips')
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


@app.route('/api/live_pose_feedback')
def live_pose_feedback():
    """Return latest live-scoring snapshot for the active webcam stream."""
    feedback_data = deepcopy(LATEST_FEEDBACK)
    # Prepare voice instruction from tips
    if feedback_data.get('tips') and len(feedback_data['tips']) > 0:
        feedback_data['voice_instruction'] = feedback_data['tips'][0]
    else:
        feedback_data['voice_instruction'] = ''
    return jsonify({'status': 'ok', 'data': feedback_data})


@app.route('/api/save_progress', methods=['POST'])
def save_progress():
    """Save user's pose detection session to their history"""
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
    try:
        data = request.json
        pose = data.get('pose')
        score = data.get('score', 0)
        duration = data.get('duration', 0)
        
        username = session['username']
        users = load_users()
        user = next((u for u in users if u['username'] == username), None)
        
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
        # Add session to history
        if 'history' not in user:
            user['history'] = []
        
        session_entry = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'pose': pose,
            'score': float(score),
            'duration': int(duration)
        }
        
        user['history'].append(session_entry)
        save_users(users)
        
        return jsonify({'status': 'success', 'message': 'Progress saved'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


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
