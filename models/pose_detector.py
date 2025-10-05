"""
Yoga Pose Detection Model
This module contains the core pose detection and classification logic.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Dict, List, Tuple, Optional


class PoseDetector:
    """
    A class to detect and analyze yoga poses using MediaPipe.
    """
    
    def __init__(self, 
                 min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        """
        Initialize the pose detector.
        
        Args:
            min_detection_confidence: Minimum confidence for pose detection
            min_tracking_confidence: Minimum confidence for pose tracking
        """
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
    
    def find_pose(self, image: np.ndarray, draw: bool = True) -> Tuple[np.ndarray, Optional[object]]:
        """
        Detect pose in an image.
        
        Args:
            image: Input image in BGR format
            draw: Whether to draw landmarks on the image
            
        Returns:
            Processed image and pose results
        """
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        
        # Process the image
        results = self.pose.process(image_rgb)
        
        # Convert back to BGR
        image_rgb.flags.writeable = True
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        
        # Draw landmarks if requested and detected
        if draw and results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
            )
        
        return image, results
    
    def get_position(self, results, image_shape: Tuple[int, int, int]) -> List[Dict]:
        """
        Extract landmark positions from pose results.
        
        Args:
            results: MediaPipe pose results
            image_shape: Shape of the input image (height, width, channels)
            
        Returns:
            List of landmark dictionaries with id, x, y, z coordinates
        """
        landmarks = []
        if results.pose_landmarks:
            h, w, c = image_shape
            for id, lm in enumerate(results.pose_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append({
                    'id': id,
                    'x': cx,
                    'y': cy,
                    'z': lm.z,
                    'visibility': lm.visibility
                })
        return landmarks
    
    def calculate_angle(self, point1: Dict, point2: Dict, point3: Dict) -> float:
        """
        Calculate the angle between three points.
        
        Args:
            point1: First point (shoulder)
            point2: Middle point (elbow/joint)
            point3: Third point (wrist)
            
        Returns:
            Angle in degrees
        """
        # Extract coordinates
        x1, y1 = point1['x'], point1['y']
        x2, y2 = point2['x'], point2['y']
        x3, y3 = point3['x'], point3['y']
        
        # Calculate angle
        radians = np.arctan2(y3 - y2, x3 - x2) - np.arctan2(y1 - y2, x1 - x2)
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
        
        return angle
    
    def classify_pose(self, landmarks: List[Dict]) -> str:
        """
        Classify the yoga pose based on landmark positions.
        This is a simple classifier - can be extended with ML models.
        
        Args:
            landmarks: List of landmark positions
            
        Returns:
            Name of the detected pose
        """
        if not landmarks or len(landmarks) < 33:
            return "No Pose Detected"
        
        # Example: Detect basic poses based on angles
        # This is a simplified version - real implementation would be more complex
        
        try:
            # Get key landmarks (using MediaPipe landmark indices)
            left_shoulder = landmarks[11]
            left_elbow = landmarks[13]
            left_wrist = landmarks[15]
            left_hip = landmarks[23]
            left_knee = landmarks[25]
            left_ankle = landmarks[27]
            
            right_shoulder = landmarks[12]
            right_elbow = landmarks[14]
            right_wrist = landmarks[16]
            right_hip = landmarks[24]
            right_knee = landmarks[26]
            right_ankle = landmarks[28]
            
            # Calculate some key angles
            left_arm_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
            left_leg_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
            
            # Simple classification logic (extend this with more poses)
            if left_arm_angle < 30 and left_leg_angle > 160:
                return "Mountain Pose (Tadasana)"
            elif left_leg_angle < 100:
                return "Warrior Pose"
            else:
                return "Unknown Pose"
                
        except (IndexError, KeyError):
            return "Detection Error"
    
    def close(self):
        """Release resources."""
        self.pose.close()


# Yoga pose reference data
YOGA_POSES = {
    "mountain": {
        "name": "Mountain Pose (Tadasana)",
        "difficulty": "beginner",
        "description": "Stand tall with feet together, arms at sides"
    },
    "warrior1": {
        "name": "Warrior I (Virabhadrasana I)",
        "difficulty": "beginner",
        "description": "Lunge with arms raised overhead"
    },
    "warrior2": {
        "name": "Warrior II (Virabhadrasana II)",
        "difficulty": "beginner",
        "description": "Lunge with arms extended to sides"
    },
    "tree": {
        "name": "Tree Pose (Vrksasana)",
        "difficulty": "intermediate",
        "description": "Balance on one leg with hands in prayer"
    },
    "downdog": {
        "name": "Downward Dog (Adho Mukha Svanasana)",
        "difficulty": "beginner",
        "description": "Inverted V-shape with hands and feet on ground"
    },
    "plank": {
        "name": "Plank Pose (Phalakasana)",
        "difficulty": "beginner",
        "description": "Hold body straight in push-up position"
    }
}
