@echo off
REM LeafGuard Flask App Startup Script
REM This script will install dependencies and run the Flask app

echo.
echo ============================================
echo   LeafGuard - Leaf Disease Predictor
echo   Flask Application Startup
echo ============================================
echo.

REM Change to the app directory
cd /d "%~dp0"

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Installing/Updating dependencies...
echo This may take a few minutes on first run...
echo.

REM Install basic Flask dependencies first
echo Installing Flask...
pip install Flask Werkzeug --quiet

echo Installing ML/Data Science libraries...
pip install numpy opencv-python scikit-learn xgboost Pillow --quiet

echo Installing TensorFlow (this may take several minutes)...
pip install tensorflow --quiet

echo.
echo Dependencies installation completed!
echo.
echo ============================================
echo   Starting Flask Application...
echo ============================================
echo.
echo The application will be available at:
echo   http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the Flask app
python app.py

pause
