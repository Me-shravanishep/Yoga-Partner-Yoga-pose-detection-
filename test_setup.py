"""
Test script to verify all components are working
Run this after installing dependencies to check your setup
"""

import sys


def test_imports():
    """Test if all required libraries can be imported"""
    print("Testing imports...")
    
    try:
        import flask
        print("✓ Flask imported successfully -", flask.__version__)
    except ImportError as e:
        print("✗ Flask import failed:", e)
        return False
    
    try:
        import cv2
        print("✓ OpenCV imported successfully -", cv2.__version__)
    except ImportError as e:
        print("✗ OpenCV import failed:", e)
        return False
    
    try:
        import mediapipe as mp
        version = getattr(mp, '__version__', 'version unknown')
        print("✓ MediaPipe imported successfully -", version)
    except ImportError as e:
        print("✗ MediaPipe import failed:", e)
        return False
    
    try:
        import numpy as np
        print("✓ NumPy imported successfully -", np.__version__)
    except ImportError as e:
        print("✗ NumPy import failed:", e)
        return False
    
    try:
        import pyttsx3
        print("✓ pyttsx3 imported successfully")
    except ImportError as e:
        print("✗ pyttsx3 import failed:", e)
        print("  (This is optional - only needed for voice features)")
    
    return True


def test_camera():
    """Test if camera is accessible"""
    print("\nTesting camera access...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ Camera cannot be opened")
            print("  - Check if another app is using the camera")
            print("  - Verify camera permissions in Windows settings")
            return False
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            print("✗ Cannot read frame from camera")
            return False
        
        h, w = frame.shape[:2]
        print(f"✓ Camera accessible - Resolution: {w}x{h}")
        return True
        
    except Exception as e:
        print("✗ Camera test failed:", e)
        return False


def test_pose_detector():
    """Test if PoseDetector class can be instantiated"""
    print("\nTesting PoseDetector class...")
    
    try:
        from models.pose_detector import PoseDetector, YOGA_POSES
        
        detector = PoseDetector()
        print("✓ PoseDetector instantiated successfully")
        
        print(f"✓ Yoga poses database loaded - {len(YOGA_POSES)} poses available")
        
        detector.close()
        return True
        
    except Exception as e:
        print("✗ PoseDetector test failed:", e)
        return False


def test_flask_app():
    """Test if Flask app can be imported"""
    print("\nTesting Flask app...")
    
    try:
        import app
        print("✓ app.py imported successfully")
        print(f"✓ Flask app configured with {len(app.app.url_map._rules)} routes")
        return True
        
    except Exception as e:
        print("✗ Flask app test failed:", e)
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Yoga Pose Detection - System Test")
    print("=" * 60)
    print(f"Python version: {sys.version}")
    print()
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Camera", test_camera()))
    results.append(("PoseDetector", test_pose_detector()))
    results.append(("Flask App", test_flask_app()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:20s} - {status}")
    
    print("=" * 60)
    
    if all(result[1] for result in results):
        print("\n🎉 All tests passed! You're ready to run the application.")
        print("\nNext steps:")
        print("1. Run: python app.py")
        print("2. Open: http://127.0.0.1:5000/")
        print("3. Click 'Start Detection' to begin pose tracking")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("- Install missing dependencies: pip install -r requirements.txt")
        print("- Check camera permissions in Windows Settings")
        print("- Make sure Python 3.10 or 3.11 is being used")
        return 1


if __name__ == "__main__":
    exit(main())
