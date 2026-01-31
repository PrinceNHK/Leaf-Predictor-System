"""
Test script to verify Flask app configuration
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

try:
    print("=" * 50)
    print("LeafGuard Flask App - Verification")
    print("=" * 50)
    
    print("\n1. Testing Flask import...")
    from flask import Flask
    print("   ✓ Flask imported successfully")
    
    print("\n2. Testing OpenCV import...")
    import cv2
    print("   ✓ OpenCV imported successfully")
    
    print("\n3. Testing NumPy import...")
    import numpy as np
    print("   ✓ NumPy imported successfully")
    
    print("\n4. Testing XGBoost import...")
    from xgboost import XGBClassifier
    print("   ✓ XGBoost imported successfully")
    
    print("\n5. Testing scikit-learn import...")
    from sklearn.preprocessing import LabelEncoder
    print("   ✓ scikit-learn imported successfully")
    
    print("\n6. Testing Flask app creation...")
    app = Flask(__name__)
    print("   ✓ Flask app created successfully")
    
    print("\n7. Checking model files...")
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = {
        'cnn_feature_extractor.h5': os.path.join(base_path, 'cnn_feature_extractor.h5'),
        'xgb_classifier_model.json': os.path.join(base_path, 'xgb_classifier_model.json'),
        'label_encoder_classes.npy': os.path.join(base_path, 'label_encoder_classes.npy')
    }
    
    missing_files = []
    for name, path in files.items():
        if os.path.exists(path):
            size = os.path.getsize(path) / 1024 / 1024  # Convert to MB
            print(f"   ✓ {name} ({size:.1f} MB)")
        else:
            print(f"   ✗ {name} - NOT FOUND")
            missing_files.append(name)
    
    print("\n" + "=" * 50)
    
    if not missing_files:
        print("✓ All checks passed! App is ready to run.")
        print("\nStart the app with:")
        print("  python app.py")
        sys.exit(0)
    else:
        print(f"⚠ Missing model files: {', '.join(missing_files)}")
        print("\nPlease ensure these files are in the parent directory:")
        for filename in missing_files:
            print(f"  - {filename}")
        sys.exit(1)
        
except Exception as e:
    print(f"\n✗ Error during verification: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
