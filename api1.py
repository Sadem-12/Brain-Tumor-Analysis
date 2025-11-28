from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import json
import datetime
import logging
import secrets
from functools import wraps
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
try:
    from preprocessing import resize_and_normalize
    from main import predict_tumor, generate_report
    TENSORFLOW_AVAILABLE = True
except ImportError as e:
    print(f"Warning: TensorFlow not available: {e}")
    TENSORFLOW_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit
API_KEYS = os.environ.get('API_KEYS', '').split(',') if os.environ.get('API_KEYS') else []

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip authentication if no API keys are configured (development mode)
        if not API_KEYS:
            return f(*args, **kwargs)

        # Get API key from header
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({'error': 'API key required'}), 401

        # Validate API key
        if api_key not in API_KEYS:
            logger.warning(f'Invalid API key attempt: {api_key[:10]}...')
            return jsonify({'error': 'Invalid API key'}), 401

        return f(*args, **kwargs)
    return decorated_function

def validate_scan_id(scan_id):
    """Validate scan_id format"""
    try:
        uuid.UUID(scan_id)
        return True
    except ValueError:
        return False

def log_request_info():
    """Log request information for security monitoring"""
    logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_model(image_path):
    """
    Shared function for AI team - runs the model on given image path
    Returns prediction results in the format expected by the API
    """
    if not TENSORFLOW_AVAILABLE:
        # Return mock data for testing when TensorFlow is not available
        return {
            "tumor_type": "glioma",
            "confidence": 0.93,
            "predictions": {
                "glioma": 93.0,
                "meningioma": 5.0,
                "notumor": 1.0,
                "pituitary": 1.0
            }
        }

    try:
        predicted_class, confidence, predictions = predict_tumor(image_path)

        return {
            "tumor_type": predicted_class,
            "confidence": confidence / 100,  # Convert to decimal format
            "predictions": {
                class_name: pred * 100 for class_name, pred in zip(
                    ['glioma', 'meningioma', 'notumor', 'pituitary'], predictions
                )
            }
        }
    except Exception as e:
        raise Exception(f"Model prediction failed: {str(e)}")

@app.route('/upload', methods=['POST'])
@require_api_key
def upload_file():
    """Upload MRI image file"""
    try:
        log_request_info()
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file part in the request'
            }), 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'error': 'No file selected'
            }), 400

        # Validate file extension
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'File type not allowed. Please upload PNG, JPG, JPEG, or GIF files only.'
            }), 400

        # Generate unique scan ID
        scan_id = str(uuid.uuid4())

        # Secure filename and save
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{scan_id}_{filename}")
        file.save(file_path)

        return jsonify({
            'message': 'File uploaded successfully',
            'scan_id': scan_id,
            'file_path': file_path
        }), 200

    except Exception as e:
        return jsonify({
            'error': f'Upload failed: {str(e)}'
        }), 500

@app.route('/analyze', methods=['POST'])
@require_api_key
def analyze_image():
    """Analyze uploaded MRI image"""
    try:
        log_request_info()

        # Get scan_id from request
        data = request.get_json()
        if not data or 'scan_id' not in data:
            return jsonify({
                'error': 'scan_id is required in request body'
            }), 400

        scan_id = data['scan_id']

        # Validate scan_id format
        if not validate_scan_id(scan_id):
            return jsonify({
                'error': 'Invalid scan_id format'
            }), 400

        # Find the uploaded file
        upload_dir = app.config['UPLOAD_FOLDER']
        uploaded_files = [f for f in os.listdir(upload_dir) if f.startswith(scan_id + '_')]

        if not uploaded_files:
            return jsonify({
                'error': f'No uploaded file found for scan_id: {scan_id}'
            }), 404

        # Get the file path
        file_path = os.path.join(upload_dir, uploaded_files[0])

        # Run model analysis
        model_result = run_model(file_path)

        # Generate detailed report
        report = generate_report(
            model_result['tumor_type'],
            model_result['confidence'] * 100,  # Convert back to percentage for report
            [pred / 100 for pred in model_result['predictions'].values()]  # Convert back to decimal for report
        )

        # Create result object
        result = {
            'scan_id': scan_id,
            'timestamp': datetime.datetime.now().isoformat(),
            'image_path': file_path,
            'analysis': model_result,
            'report': report
        }

        # Save result to file
        result_file = os.path.join(app.config['RESULTS_FOLDER'], f"{scan_id}_result.json")
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            'error': f'Analysis failed: {str(e)}'
        }), 500

@app.route('/result/<scan_id>', methods=['GET'])
@require_api_key
def get_result(scan_id):
    """Retrieve analysis result by scan_id"""
    try:
        log_request_info()

        # Validate scan_id format
        if not validate_scan_id(scan_id):
            return jsonify({
                'error': 'Invalid scan_id format'
            }), 400
        # Look for result file
        result_file = os.path.join(app.config['RESULTS_FOLDER'], f"{scan_id}_result.json")

        if not os.path.exists(result_file):
            return jsonify({
                'error': f'No result found for scan_id: {scan_id}'
            }), 404

        # Read and return result
        with open(result_file, 'r') as f:
            result = json.load(f)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            'error': f'Failed to retrieve result: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat()
    }), 200

@app.route('/generate-api-key', methods=['POST'])
def generate_api_key():
    """Generate a new API key (for admin use)"""
    try:
        # In production, this should require admin authentication
        new_api_key = secrets.token_hex(32)

        # Add to environment variable (in production, save to secure storage)
        current_keys = os.environ.get('API_KEYS', '')
        updated_keys = f"{current_keys},{new_api_key}" if current_keys else new_api_key
        os.environ['API_KEYS'] = updated_keys

        logger.info(f"New API key generated: {new_api_key[:10]}...")

        return jsonify({
            'api_key': new_api_key,
            'message': 'API key generated successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'error': f'Failed to generate API key: {str(e)}'
        }), 500

@app.route('/api-keys', methods=['GET'])
def list_api_keys():
    """List current valid API keys (for development/debugging)"""
    try:
        current_keys = os.environ.get('API_KEYS', '')
        if current_keys:
            keys = current_keys.split(',')
            # Return only first 10 characters of each key for security
            safe_keys = [key[:10] + '...' if len(key) > 10 else key for key in keys]
            return jsonify({
                'valid_keys_preview': safe_keys,
                'count': len(keys)
            }), 200
        else:
            return jsonify({
                'valid_keys_preview': [],
                'count': 0,
                'message': 'No API keys configured'
            }), 200

    except Exception as e:
        return jsonify({
            'error': f'Failed to list API keys: {str(e)}'
        }), 500

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(error):
    """Handle file size limit exceeded"""
    return jsonify({
        'error': 'File too large. Maximum size allowed is 10MB.'
    }), 413

@app.errorhandler(500)
def handle_internal_error(error):
    """Handle internal server errors"""
    logger.error(f'Internal server error: {str(error)}')
    return jsonify({
        'error': 'Internal server error occurred'
    }), 500

if __name__ == '__main__':
    # Generate a default API key if none exist
    if not API_KEYS:
        default_key = secrets.token_hex(32)
        os.environ['API_KEYS'] = default_key
        print(f"Default API Key: {default_key}")
        print("Please save this key securely for API access.")

    app.run(debug=True, host='0.0.0.0', port=5000)