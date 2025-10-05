from flask import Flask, render_template, Response, jsonify, request
import cv2
import numpy as np
import json
import os
from datetime import datetime

app = Flask(__name__)

# Configure upload folder and data folder
UPLOAD_FOLDER = 'static/uploads'
DATA_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Note: MediaPipe requires Python 3.10 or 3.11
# This version works without MediaPipe for demonstration
# To use pose detection, install Python 3.11 and reinstall dependencies


@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint - returns versions of installed libraries"""
    versions = {
        'opencv': cv2.__version__,
        'mediapipe': 'Not installed (requires Python 3.10 or 3.11)',
        'numpy': np.__version__,
        'note': 'Install Python 3.11 for full MediaPipe pose detection'
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
    return jsonify({'width': w, 'height': h, 'note': 'Camera works! Install Python 3.11 for pose detection.'})


@app.route('/video_feed')
def video_feed():
    """Video streaming route - returns MJPEG stream (without pose detection for now)"""
    def generate():
        cap = cv2.VideoCapture(0)
        while True:
            success, frame = cap.read()
            if not success:
                break
            
            # Add text overlay indicating MediaPipe is not available
            cv2.putText(frame, 'Camera Feed Working!', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, 'Install Python 3.11 for pose detection', (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        cap.release()
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


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
    print("=" * 60)
    print("Yoga Pose Detection Server Starting...")
    print("=" * 60)
    print("Note: This version runs without MediaPipe pose detection")
    print("To enable pose detection:")
    print("1. Install Python 3.11 from https://www.python.org/downloads/")
    print("2. Create new venv: py -3.11 -m venv venv")
    print("3. Install requirements: pip install -r requirements.txt")
    print("=" * 60)
    print("Server will start at: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
