#!/bin/bash
# LeafGuard Flask App Startup Script for macOS/Linux

echo ""
echo "============================================"
echo "  LeafGuard - Leaf Disease Predictor"
echo "  Flask Application Startup"
echo "============================================"
echo ""

# Change to the app directory
cd "$(dirname "$0")"

echo "Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python3 is not installed"
    exit 1
fi

echo ""
echo "Installing/Updating dependencies..."
echo "This may take a few minutes on first run..."
echo ""

# Install basic Flask dependencies first
echo "Installing Flask..."
pip3 install Flask Werkzeug --quiet

echo "Installing ML/Data Science libraries..."
pip3 install numpy opencv-python scikit-learn xgboost Pillow --quiet

echo "Installing TensorFlow (this may take several minutes)..."
pip3 install tensorflow --quiet

echo ""
echo "Dependencies installation completed!"
echo ""
echo "============================================"
echo "  Starting Flask Application..."
echo "============================================"
echo ""
echo "The application will be available at:"
echo "  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the Flask app
python3 app.py
