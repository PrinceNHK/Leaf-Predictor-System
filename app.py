import os
import numpy as np
import cv2
from flask import Flask, render_template, request, jsonify, send_from_directory
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from werkzeug.utils import secure_filename
from datetime import datetime
import json

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load models
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cnn_feature_extractor = None
xgb_classifier = None
label_encoder = None

try:
    from tensorflow.keras.models import load_model
    cnn_feature_extractor = load_model(os.path.join(BASE_PATH, "cnn_feature_extractor.h5"))
    xgb_classifier = XGBClassifier()
    xgb_classifier.load_model(os.path.join(BASE_PATH, "xgb_classifier_model.json"))
    label_encoder_classes = np.load(os.path.join(BASE_PATH, "label_encoder_classes.npy"), allow_pickle=True)
    label_encoder = LabelEncoder()
    label_encoder.classes_ = label_encoder_classes
    print("✓ Models loaded successfully!")
    MODELS_LOADED = True
except Exception as e:
    print(f"✗ Warning: Models not yet available: {e}")
    print("ℹ Models will be loaded on first prediction attempt")
    MODELS_LOADED = False

# Image processing parameters
WIDTH, HEIGHT = 224, 224

# Disease information
DISEASE_INFO = {
    'bacterial spot': {
        'description': 'Bacterial spot is a common disease that affects tomato plants, causing dark, water-soaked spots on leaves.',
        'symptoms': [
            'Dark brown or black spots on leaves',
            'Spots are usually surrounded by a yellow halo',
            'Spots may coalesce and cause yellowing of entire leaves',
            'Affected leaves eventually drop from the plant'
        ],
        'causes': 'Caused by various species of Xanthomonas bacteria',
        'prevention': [
            'Use disease-resistant varieties',
            'Remove infected plant parts immediately',
            'Avoid overhead watering',
            'Apply copper fungicides as preventative measure'
        ],
        'treatment': [
            'Remove affected leaves and destroy them',
            'Apply copper or antibiotic sprays',
            'Improve air circulation around plants',
            'Do not work with wet plants'
        ]
    },
    'early blight': {
        'description': 'Early blight is a fungal disease that primarily affects lower leaves and causes target-like spots.',
        'symptoms': [
            'Circular lesions with concentric rings (target-like appearance)',
            'Spots appear on lower leaves first',
            'Brown color with yellow halo around lesions',
            'Infected leaves eventually yellow and drop'
        ],
        'causes': 'Caused by the fungus Alternaria solani',
        'prevention': [
            'Space plants properly for good air circulation',
            'Mulch around plants to prevent soil splash',
            'Remove lower leaves as plant grows',
            'Use resistant varieties when available'
        ],
        'treatment': [
            'Prune lower branches regularly',
            'Apply fungicides like mancozeb or chlorothalonil',
            'Remove and destroy infected leaves',
            'Maintain dry foliage by watering at soil level'
        ]
    },
    'healthy': {
        'description': 'Healthy leaves show no signs of disease or pest damage.',
        'symptoms': [
            'Green coloration',
            'No spots or discoloration',
            'No visible damage or yellowing',
            'Normal growth and appearance'
        ],
        'causes': 'N/A - This is a healthy plant',
        'prevention': [
            'Maintain proper watering schedule',
            'Provide adequate nutrients',
            'Ensure proper sunlight exposure',
            'Monitor regularly for early signs of disease'
        ],
        'treatment': 'No treatment needed - continue regular maintenance'
    },
    'late blight': {
        'description': 'Late blight is a serious fungal disease caused by Phytophthora infestans that can rapidly destroy tomato plants.',
        'symptoms': [
            'Water-soaked lesions on leaves and stems',
            'Lesions turn brown and may have a white moldy appearance on the underside',
            'Rapid spread during wet, cool weather',
            'Can affect the entire plant within days'
        ],
        'causes': 'Caused by the oomycete pathogen Phytophthora infestans',
        'prevention': [
            'Plant resistant varieties',
            'Ensure good air circulation',
            'Avoid overhead watering',
            'Remove infected plant material promptly'
        ],
        'treatment': [
            'Apply fungicides containing chlorothalonil or mancozeb',
            'Remove and destroy infected plants',
            'Apply preventive fungicides during wet periods',
            'Space plants wider for better air circulation'
        ]
    },
    'leaf mold': {
        'description': 'Leaf mold is a fungal disease that thrives in humid conditions and affects the underside of leaves.',
        'symptoms': [
            'Yellow spots on upper leaf surface',
            'Gray or olive-colored mold on undersides of leaves',
            'Mold appears as a fine, powdery coating',
            'Affected leaves may drop prematurely'
        ],
        'causes': 'Caused by the fungus Passalora fulva (formerly Cladosporium fulvum)',
        'prevention': [
            'Maintain low humidity levels',
            'Improve air circulation with fans or spacing',
            'Avoid overhead watering',
            'Remove lower leaves as plants grow'
        ],
        'treatment': [
            'Prune infected leaves and remove them from area',
            'Apply sulfur or copper fungicides',
            'Increase ventilation and reduce humidity',
            'Apply fungicides weekly during humid periods'
        ]
    },
    'septoria leaf spot': {
        'description': 'Septoria leaf spot is a fungal disease that causes circular spots with dark borders and gray centers.',
        'symptoms': [
            'Circular spots with dark brown borders',
            'Gray or tan center with dark ring',
            'Tiny dark bodies (pycnidia) visible in center',
            'Often starts on lower leaves and moves upward'
        ],
        'causes': 'Caused by the fungus Septoria lycopersici',
        'prevention': [
            'Use disease-free seeds and transplants',
            'Space plants for good air circulation',
            'Remove lower leaves from plants',
            'Avoid working with plants when leaves are wet'
        ],
        'treatment': [
            'Remove infected leaves immediately',
            'Apply fungicides like copper or chlorothalonil',
            'Keep foliage dry by watering at base',
            'Apply preventive sprays during wet weather'
        ]
    },
    'spider mites two-spotted spider mite': {
        'description': 'Spider mites are tiny pests that cause stippling and yellowing of leaves.',
        'symptoms': [
            'Tiny light spots on leaves (stippling)',
            'Leaves turn yellow and become papery',
            'Fine webbing may be visible on undersides',
            'Leaves may drop if infestation is severe'
        ],
        'causes': 'Caused by the two-spotted spider mite (Tetranychus urticae)',
        'prevention': [
            'Maintain adequate humidity levels',
            'Spray plants with water to disrupt spider mites',
            'Monitor plant undersides regularly',
            'Avoid excessive nitrogen fertilizer'
        ],
        'treatment': [
            'Spray with strong stream of water daily',
            'Apply insecticidal soap or neem oil',
            'Use miticides if infestation is severe',
            'Increase humidity around plants'
        ]
    },
    'target spot': {
        'description': 'Target spot is a fungal disease causing concentric circular lesions on leaves.',
        'symptoms': [
            'Circular lesions with concentric rings',
            'Dark brown outer ring with lighter center',
            'Yellow halo around the spots',
            'Affects leaves at all heights of the plant'
        ],
        'causes': 'Caused by the fungus Corynespora cassiicola',
        'prevention': [
            'Use resistant varieties',
            'Maintain good air circulation',
            'Remove infected leaves promptly',
            'Avoid overhead watering'
        ],
        'treatment': [
            'Apply fungicides like mancozeb or chlorothalonil',
            'Remove infected leaves',
            'Improve ventilation around plants',
            'Apply preventive sprays during humid periods'
        ]
    },
    'tomato mosaic virus': {
        'description': 'Tomato mosaic virus causes mottling and distortion of leaves and fruit.',
        'symptoms': [
            'Mottled, light and dark green pattern on leaves',
            'Leaf distortion and curling',
            'Yellow spots and stripes on leaves',
            'Stunted growth and reduced fruit production'
        ],
        'causes': 'Caused by the Tomato Mosaic Virus (ToMV) transmitted by contact or contaminated tools',
        'prevention': [
            'Use resistant varieties (marked TMV-resistant)',
            'Sanitize tools before working with plants',
            'Avoid handling plants when leaves are wet',
            'Remove weeds that may carry the virus'
        ],
        'treatment': [
            'Remove and destroy infected plants',
            'Sanitize all tools and equipment',
            'Wash hands before working with healthy plants',
            'No chemical treatment available - prevention is key'
        ]
    },
    'tomato yellow leaf curl virus': {
        'description': 'Tomato yellow leaf curl virus causes yellowing and curling of young leaves.',
        'symptoms': [
            'Young leaves curl upward',
            'Leaves become yellow and brittle',
            'Stunted growth and wilting',
            'Reduced or no fruit production'
        ],
        'causes': 'Caused by Tomato Yellow Leaf Curl Virus (TYLCV), primarily transmitted by whiteflies',
        'prevention': [
            'Use virus-resistant varieties',
            'Control whitefly populations with insecticides',
            'Use row covers on young plants',
            'Remove infected plants immediately'
        ],
        'treatment': [
            'Remove and destroy infected plants',
            'Control whitefly populations with appropriate insecticides',
            'Apply reflective mulches to confuse whiteflies',
            'No cure exists - focus on prevention'
        ]
    }
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(image_path):
    """Process image for model prediction"""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image not found at path: {image_path}")
    img = cv2.resize(img, (WIDTH, HEIGHT))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_disease(image_path):
    """Predict disease from image"""
    try:
        global cnn_feature_extractor, xgb_classifier, label_encoder, MODELS_LOADED
        
        if not MODELS_LOADED or cnn_feature_extractor is None:
            # Try loading models if not already loaded
            try:
                from tensorflow.keras.models import load_model
                cnn_feature_extractor = load_model(os.path.join(BASE_PATH, "cnn_feature_extractor.h5"))
                xgb_classifier = XGBClassifier()
                xgb_classifier.load_model(os.path.join(BASE_PATH, "xgb_classifier_model.json"))
                label_encoder_classes = np.load(os.path.join(BASE_PATH, "label_encoder_classes.npy"), allow_pickle=True)
                label_encoder = LabelEncoder()
                label_encoder.classes_ = label_encoder_classes
                MODELS_LOADED = True
            except Exception as load_error:
                raise Exception(f"Failed to load models: {str(load_error)}")
        
        processed_image = process_image(image_path)
        features = cnn_feature_extractor.predict(processed_image, verbose=0)
        predicted_class_idx = xgb_classifier.predict(features)[0]
        class_name = label_encoder.inverse_transform([predicted_class_idx])[0]
        
        # Get probability
        prediction_proba = xgb_classifier.predict_proba(features)[0]
        confidence = float(np.max(prediction_proba)) * 100
        
        return class_name, confidence
    except Exception as e:
        raise Exception(f"Prediction error: {str(e)}")

@app.route('/')
def home():
    """Home page with disease information"""
    diseases = []
    for disease_name, info in DISEASE_INFO.items():
        if disease_name != 'healthy':
            diseases.append({
                'name': disease_name.title(),
                'description': info['description'],
                'symptoms_count': len(info['symptoms'])
            })
    return render_template('index.html', diseases=diseases)

@app.route('/predictor')
def predictor():
    """Predictor page"""
    return render_template('predictor.html')

@app.route('/disease/<disease_name>')
def disease_detail(disease_name):
    """Disease detail page"""
    disease_key = disease_name.lower()
    if disease_key in DISEASE_INFO:
        info = DISEASE_INFO[disease_key]
        return render_template('disease_detail.html', 
                             disease_name=disease_name.title(), 
                             disease_info=info)
    return "Disease not found", 404

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for image prediction"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format. Allowed: png, jpg, jpeg, gif, bmp'}), 400
        
        # Save the file
        filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Make prediction
        disease, confidence = predict_disease(filepath)
        
        disease_info = DISEASE_INFO.get(disease, {})
        
        response = {
            'disease': disease.title(),
            'disease_key': disease,
            'confidence': round(confidence, 2),
            'description': disease_info.get('description', ''),
            'symptoms': disease_info.get('symptoms', []),
            'causes': disease_info.get('causes', ''),
            'prevention': disease_info.get('prevention', []),
            'treatment': disease_info.get('treatment', []),
            'image_path': f'/uploads/{filename}'
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large"""
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("=" * 50)
    print("🌿 Leaf Disease Predictor - Flask App")
    print("=" * 50)
    print("Starting Flask server...")
    print("Visit: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
