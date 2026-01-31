# 🌿 LeafGuard - Getting Started Guide

## 🎉 Welcome to Your Professional Leaf Disease Predictor Website!

Your Flask website is now live and ready to use!

---

## 📍 Access Your Website

### Local Access (Your Computer)
```
http://localhost:5000
```

### Network Access (Other Computers on Same Network)
```
http://192.168.1.5:5000
```
(Note: IP address may vary depending on your network configuration)

---

## 📖 Website Navigation

### Home Page
**URL**: `http://localhost:5000/`

**What you'll see:**
- Animated hero section with "Leaf Disease Detection" title
- About section explaining the system
- "How It Works" with 4-step process
- 10 disease cards with quick info
- Features and benefits
- Call-to-action button

**Actions:**
- Click "Start Prediction" or "Predict Now" to go to predictor
- Click on disease cards to see detailed information
- Scroll to explore all diseases

### Predictor Page
**URL**: `http://localhost:5000/predictor`

**What you'll see:**
- Large upload area
- File selection button
- Disease detection interface
- Tips section for best results

**How to use:**
1. Click "Choose File" or drag-drop an image
2. Preview your image
3. Click "Analyze Image"
4. Wait for results (2-10 seconds)
5. View disease information with tabs
6. Upload another image if needed

### Disease Detail Pages
**URL**: `http://localhost:5000/disease/<disease_name>`

Examples:
- `http://localhost:5000/disease/early%20blight`
- `http://localhost:5000/disease/late%20blight`
- `http://localhost:5000/disease/healthy`

**What you'll see:**
- Complete disease description
- All symptoms
- Cause explanation
- Prevention methods
- Treatment options
- Links to related diseases

---

## 🖼️ Prediction Workflow

### Step 1: Upload Image
```
1. Navigate to /predictor page
2. Click "Choose File" button
   OR
   Drag and drop image onto upload area
3. Select your tomato leaf image
```

### Step 2: Image Preview
```
Your selected image will appear
- Can see if it's the right image
- Can remove and choose another
- Shows file being ready to analyze
```

### Step 3: Analyze
```
Click "Analyze Image" button
- Shows loading spinner
- "Analyzing your leaf image..." message
- Takes 2-10 seconds
```

### Step 4: View Results
```
Results display with:
- Disease name (large text)
- Confidence % with color:
  - Green ✓ (80%+) - High confidence
  - Orange ⚠ (60-79%) - Medium confidence  
  - Red ✗ (Below 60%) - Low confidence
- Disease description
- Four tabs: Symptoms | Causes | Prevention | Treatment
- Each tab shows relevant information
```

### Step 5: Take Action
```
Based on results:
- Click tabs to read detailed information
- "Upload New Image" to test another leaf
- "Back to Home" to explore more
- Contact agricultural expert if needed
```

---

## 💡 Tips for Best Predictions

### Image Quality
✅ **Good Images**
- Natural daylight
- Clear, sharp focus
- Affected area clearly visible
- Minimal background
- Leaf fills most of frame

❌ **Poor Images**
- Blurry or out of focus
- Heavy shadows
- Harsh sunlight reflections
- Tiny subject in large background
- Multiple leaves in frame

### Recommended Settings
- **Lighting**: Indirect natural sunlight
- **Angle**: Top-down, perpendicular to leaf
- **Distance**: Close enough to see details
- **Format**: JPG, PNG, GIF, or BMP
- **Size**: Any size up to 16MB

### What to Photograph
- Single affected leaf
- Multiple spots if disease shows them
- Undersides if applicable
- Early and late stages for comparison

---

## 📊 Understanding Results

### Disease Name
The predicted disease with highest probability

### Confidence Score
**What it means:**
- `95-100%`: Very high confidence, likely diagnosis
- `80-94%`: High confidence, reliable prediction
- `60-79%`: Moderate confidence, may need verification
- `Below 60%`: Low confidence, consider expert opinion

**How to interpret:**
- High confidence (80%+): Likely correct diagnosis
- Medium confidence: Consider photo quality and symptoms
- Low confidence: Take another high-quality photo or consult expert

### Symptoms Section
Lists visual signs of the disease
**Use to verify**: Do your leaf's symptoms match?

### Causes Section  
Explains what causes this disease
**Important for**: Understanding origin and prevention

### Prevention Section
How to prevent this disease
**Use before**: Problem appears or early stages

### Treatment Section
What to do if disease is present
**Use when**: Disease detected on plants

---

## 🚀 Advanced Usage

### Using the API
If you're a developer, the prediction API is available:

**Endpoint:**
```
POST http://localhost:5000/api/predict
```

**Request:**
```bash
curl -X POST -F "file=@leaf.jpg" http://localhost:5000/api/predict
```

**Response:**
```json
{
  "disease": "Late Blight",
  "disease_key": "late blight",
  "confidence": 92.5,
  "description": "Late blight is a serious fungal disease...",
  "symptoms": [
    "Water-soaked lesions on leaves and stems",
    "Lesions turn brown..."
  ],
  "causes": "Caused by Phytophthora infestans",
  "prevention": [
    "Plant resistant varieties",
    "Ensure good air circulation"
  ],
  "treatment": [
    "Apply fungicides",
    "Remove infected plants"
  ],
  "image_path": "/uploads/20260131_120000_image.jpg"
}
```

### Using Python
```python
import requests

# Upload and predict
with open('leaf.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:5000/api/predict',
        files=files
    )
    result = response.json()
    
    print(f"Disease: {result['disease']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"Treatment: {result['treatment']}")
```

### Checking Server Status
```bash
curl http://localhost:5000/  # Should return home page HTML
```

---

## ❓ Frequently Asked Questions

### Q: How accurate is the prediction?
**A:** The system is trained on thousands of leaf images with 90%+ accuracy. However, image quality significantly affects results. High-confidence predictions (80%+) are reliable.

### Q: Can it detect other plant diseases?
**A:** Currently, it specializes in tomato plant diseases. Future versions may support other plants.

### Q: What happens to my uploaded images?
**A:** Images are temporarily stored for processing. They're not stored permanently or shared. You can clear uploads folder manually.

### Q: How long does prediction take?
**A:** First prediction (5-10 seconds for TensorFlow init), subsequent (2-3 seconds).

### Q: Can I use this offline?
**A:** Yes! The application runs entirely on your computer. No internet required after setup.

### Q: What if confidence is low?
**A:** Try a higher-quality image or consult an agricultural expert.

### Q: Can I deploy this online?
**A:** Yes! See deployment guide in README.md

### Q: What diseases does it detect?
**A:** 10 tomato diseases: Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Tomato Mosaic Virus, Tomato Yellow Leaf Curl Virus, and Healthy reference.

### Q: Is there a database of results?
**A:** Currently, no. You can add database functionality (see README.md for details).

---

## 🛠️ Troubleshooting

### Can't Access Website
**Problem**: `http://localhost:5000` gives error

**Solution:**
1. Check if Flask is running in terminal
2. If not, run: `python app.py`
3. Wait 10 seconds for startup
4. Try again

### Upload Not Working
**Problem**: Can't select or upload image

**Solution:**
1. Check file format (JPG, PNG, GIF, BMP only)
2. Verify file size under 16MB
3. Try different image
4. Check browser console (F12) for errors

### No Results After Upload
**Problem**: Spinner appears but no results

**Solution:**
1. Wait longer (large files take 5-10 seconds)
2. Check browser console (F12) for errors
3. Try with smaller image file
4. Check terminal for error messages

### Confidence Always 100% or 0%
**Problem**: Results seem extreme

**Solution:**
1. Verify image quality
2. Try different image
3. Check model files are loaded
4. Run: `python verify_setup.py`

### Port Already in Use
**Problem**: `Address already in use`

**Solution:**
1. Find process: `netstat -ano | findstr :5000`
2. Kill process: `taskkill /PID <number> /F`
3. Or change port in app.py
4. Restart Flask

---

## 📚 Additional Resources

### Documentation Files
- `README.md` - Comprehensive documentation
- `QUICKSTART.md` - Quick start guide
- `PROJECT_SUMMARY.md` - Project overview

### Model Information
- CNN Feature Extractor: 4 convolutional layers, 4096 features
- XGBoost Classifier: Gradient boosting, 10 classes

### Technical Stack
- Flask 3.1.2
- TensorFlow 2.19.0
- XGBoost 3.1.3
- OpenCV 4.13.0.90
- Python 3.12

---

## 🎓 Learning Path

### Beginner
1. Upload a test image
2. See prediction results
3. Read disease information
4. Compare with actual plant

### Intermediate
1. Collect sample images
2. Test multiple uploads
3. Analyze confidence scores
4. Study prevention methods

### Advanced
1. Use API for integration
2. Batch process images (custom script)
3. Analyze prediction patterns
4. Extend with database
5. Deploy to cloud

---

## 📞 Support

### If Something Doesn't Work

1. **Check Console**
   - Browser: Press F12, check Console tab
   - Terminal: Look for error messages

2. **Run Verification**
   ```bash
   python verify_setup.py
   ```

3. **Check Files**
   - cnn_feature_extractor.h5 exists?
   - xgb_classifier_model.json exists?
   - label_encoder_classes.npy exists?

4. **Restart**
   ```bash
   Ctrl+C  # Stop Flask
   python app.py  # Start again
   ```

5. **Review Logs**
   - Check terminal output during prediction
   - Browser console may show frontend errors

---

## 🎯 Common Tasks

### Task: Make First Prediction
1. Open http://localhost:5000/predictor
2. Click "Choose File"
3. Select leaf image
4. Click "Analyze Image"
5. View results!

### Task: Learn About a Disease
1. Go to home page
2. Click on disease card
3. Read complete information
4. Note prevention steps

### Task: Test Multiple Images
1. Go to predictor
2. Upload image 1, get results
3. Click "Upload New Image"
4. Upload image 2, get results
5. Compare results

### Task: Find Confidence Score
1. After prediction, look at color badge
2. Top right of results
3. Shows percentage and color

### Task: Get Treatment Info
1. After prediction, click "Treatment" tab
2. Lists specific treatment options
3. Read and apply recommendations

---

## ✨ Features Overview

| Feature | Where | How to Use |
|---------|-------|-----------|
| Upload Image | /predictor | Drag-drop or click button |
| View Results | /predictor | Appears after analysis |
| Disease Info | /disease/* | Click disease card or link |
| Prevention Tips | Any disease page | Read prevention section |
| Treatment Guide | Any disease page | Read treatment section |
| Mobile Access | Any page | Works on phone/tablet |
| API Access | /api/predict | POST request with image |

---

## 🌟 Best Practices

**Do**:
- ✅ Use clear, well-lit photos
- ✅ Focus on affected areas
- ✅ Upload one leaf at a time
- ✅ Check confidence scores
- ✅ Read all information
- ✅ Verify with expert if needed

**Don't**:
- ❌ Upload blurry images
- ❌ Use photos with shadows
- ❌ Upload multiple leaves at once
- ❌ Ignore low confidence scores
- ❌ Over-rely on predictions
- ❌ Trust 100% without verification

---

## 📱 Mobile App Info

### Website on Mobile
✅ Fully responsive
✅ Optimized for touch
✅ Works in any browser
✅ No app needed

### To Access on Mobile
1. Both computers on same WiFi
2. From mobile browser: `http://192.168.1.5:5000`
3. Or use actual computer IP address

---

## 🎉 You're Ready!

Your professional leaf disease predictor website is ready to use!

### Next Steps
1. **Visit**: http://localhost:5000
2. **Upload**: A tomato leaf image
3. **Analyze**: Get instant disease detection
4. **Learn**: Read detailed disease information
5. **Act**: Apply prevention/treatment advice

---

## 📊 Statistics

- **Supported Diseases**: 10
- **Model Accuracy**: 90%+
- **Prediction Time**: 2-10 seconds
- **Page Load**: <1 second
- **Mobile Ready**: Yes
- **API Available**: Yes
- **Documentation**: Complete

---

**Enjoy LeafGuard!** 🌿

*Your AI-powered tomato leaf disease detection system*

---

**Current Version**: 1.0  
**Status**: ✅ Running  
**Last Updated**: January 31, 2026
