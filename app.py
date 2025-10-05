from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
import numpy as np

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/health')
def health():
    versions = {
        'opencv': cv2.__version__,
        'mediapipe': getattr(mp, '__version__', 'unknown'),
        'numpy': np.__version__,
    }
    return jsonify({'status': 'ok', 'versions': versions})


@app.route('/capture')
def capture_once():
    # capture a single frame from default camera and return its size as a quick test
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return jsonify({'error': 'cannot open camera'}), 500
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return jsonify({'error': 'failed to read frame'}), 500
    h, w = frame.shape[:2]
    return jsonify({'width': w, 'height': h})


if __name__ == '__main__':
    app.run(debug=True)
