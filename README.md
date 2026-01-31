# LeafGuard - Flask Disease Detector Setup Guide

## Project Structure

```
flask_app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── index.html       # Home page
│   ├── predictor.html   # Prediction page
│   ├── disease_detail.html
│   ├── 404.html
│   └── 500.html
├── static/              # Static files
│   ├── css/
│   │   └── style.css    # Professional styling
│   ├── js/
│   │   └── script.js    # Interactive features
│   ├── images/          # Images folder
│   └── uploads/         # User uploaded images (auto-created)
```

## Installation Steps

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 2. Navigate to Flask App Directory
```bash
cd "C:\Users\haris\Downloads\image data\flask_app"
```

### 3. Create Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Ensure Model Files are Present
Make sure these files are in the parent directory:
- `cnn_feature_extractor.h5`
- `xgb_classifier_model.json`
- `label_encoder_classes.npy`

### 6. Run the Application
```bash
python app.py
```

### 7. Access the Website
Open your browser and navigate to:
```
http://localhost:5000
```

## Features

✅ **Home Page**
- Disease information and overview
- About section explaining how the system works
- Steps showing the prediction process
- List of all detectable diseases
- Professional design with animations

✅ **Predictor Page**
- Drag and drop image upload
- Real-time image preview
- AI-powered disease detection
- Confidence score display
- Detailed disease information with:
  - Symptoms
  - Causes
  - Prevention methods
  - Treatment options

✅ **Disease Detail Pages**
- Comprehensive information for each disease
- Links to related diseases
- Easy navigation

✅ **Professional Features**
- Responsive design (works on mobile, tablet, desktop)
- Smooth animations and transitions
- Modern UI with gradient backgrounds
- Interactive elements
- Error handling and validation
- Loading indicators
- Success/failure feedback

## Technology Stack

- **Backend**: Flask (Python web framework)
- **ML Models**: 
  - CNN (Convolutional Neural Network) for feature extraction
  - XGBoost for classification
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Image Processing**: OpenCV, Pillow

## How It Works

1. User uploads a tomato leaf image
2. Image is processed and resized to 224x224 pixels
3. CNN extracts features from the image
4. XGBoost classifier predicts the disease
5. System returns:
   - Disease name
   - Confidence percentage
   - Detailed information about the disease
   - Prevention and treatment recommendations

## Supported Diseases

1. Bacterial Spot
2. Early Blight
3. Healthy
4. Late Blight
5. Leaf Mold
6. Septoria Leaf Spot
7. Spider Mites (Two-spotted spider mite)
8. Target Spot
9. Tomato Mosaic Virus
10. Tomato Yellow Leaf Curl Virus

## Tips for Best Results

📸 **Image Requirements**
- Clear, well-lit photos
- Close-up of the affected leaf area
- Focus on the leaf, not blurry
- Avoid shadows and reflections
- JPG, PNG, GIF, or BMP format
- Maximum file size: 16MB

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Model Loading Errors
- Ensure model files are in the correct directory
- Check file permissions
- Verify files haven't been corrupted

### Image Upload Issues
- Check file format (must be image)
- Verify file size is under 16MB
- Ensure sufficient disk space in uploads folder

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

## Performance Notes

- First prediction may take a few seconds (model initialization)
- Subsequent predictions are faster
- The system processes images locally for privacy
- Uploaded images are stored temporarily and can be cleared

## Security

- File upload validation
- File size limits (16MB)
- Secure filename handling
- Input validation
- CSRF protection possible (can be added with Flask-WTF)

## Future Enhancements

- User authentication
- Prediction history
- Batch image processing
- Model version comparison
- Export reports
- Mobile app version
- More plant types
- Multi-language support

## Support

For issues or questions, check:
1. Console output for error messages
2. Browser console (F12) for frontend errors
3. Verify all dependencies are installed
4. Ensure model files exist and are readable

---

**Enjoy using LeafGuard! 🌿**
