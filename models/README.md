# Models Folder

This folder contains the pose detection and classification models for the Yoga Pose Detection application.

## Files

### `pose_detector.py`
Core module for yoga pose detection using MediaPipe and OpenCV.

**Key Classes:**
- `PoseDetector`: Main class for pose detection and analysis

**Key Methods:**
- `find_pose(image, draw)`: Detects pose landmarks in an image
- `get_position(results, image_shape)`: Extracts landmark coordinates
- `calculate_angle(point1, point2, point3)`: Calculates angles between joints
- `classify_pose(landmarks)`: Classifies detected pose

**Usage Example:**
```python
from models.pose_detector import PoseDetector

# Initialize detector
detector = PoseDetector()

# Process an image
image, results = detector.find_pose(frame, draw=True)

# Get landmark positions
landmarks = detector.get_position(results, frame.shape)

# Classify the pose
pose_name = detector.classify_pose(landmarks)

print(f"Detected pose: {pose_name}")
```

## Yoga Poses Reference

The module includes reference data for common yoga poses:
- Mountain Pose (Tadasana) - Beginner
- Warrior I & II (Virabhadrasana) - Beginner
- Tree Pose (Vrksasana) - Intermediate
- Downward Dog (Adho Mukha Svanasana) - Beginner
- Plank Pose (Phalakasana) - Beginner

## Future Enhancements

1. **ML-based Classification**: Train a machine learning model on yoga pose datasets
2. **Real-time Feedback**: Provide audio/visual feedback for pose correction
3. **Pose Sequences**: Detect and track yoga flow sequences
4. **Difficulty Scoring**: Score pose accuracy based on ideal angles
5. **Custom Pose Training**: Allow users to add custom poses

## Dependencies

- OpenCV (`opencv-python`)
- MediaPipe (`mediapipe`)
- NumPy (`numpy`)
