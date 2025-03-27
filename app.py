import os
import logging
from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
import tempfile
import uuid
from werkzeug.utils import secure_filename

from ocr_processor import preprocess_image, perform_ocr
from nlp_processor import extract_medical_terms
from hcc_mapper import map_to_hcc_codes

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Configure upload settings
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'document' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)
    
    file = request.files['document']
    
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Generate a unique filename
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save the file
        file.save(filepath)
        logger.debug(f"File saved at: {filepath}")
        
        try:
            # Process the document
            preprocessed_image = preprocess_image(filepath, file_extension)
            extracted_text = perform_ocr(preprocessed_image)
            
            if not extracted_text:
                flash('No text could be extracted from the document', 'warning')
                return redirect(url_for('index'))
            
            # Extract medical terms
            medical_terms = extract_medical_terms(extracted_text)
            
            # Map to HCC codes
            hcc_codes = map_to_hcc_codes(medical_terms)
            
            # Store results in session
            session['extracted_text'] = extracted_text
            session['medical_terms'] = medical_terms
            session['hcc_codes'] = hcc_codes
            session['original_filename'] = original_filename
            
            return redirect(url_for('show_results'))
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            flash(f'Error processing document: {str(e)}', 'danger')
            return redirect(url_for('index'))
        finally:
            # Clean up the uploaded file
            try:
                os.remove(filepath)
            except Exception as e:
                logger.error(f"Error removing temporary file: {str(e)}")
    
    else:
        flash(f'Allowed file types are: {", ".join(ALLOWED_EXTENSIONS)}', 'warning')
        return redirect(request.url)

@app.route('/results')
def show_results():
    # Get results from session
    extracted_text = session.get('extracted_text', '')
    medical_terms = session.get('medical_terms', [])
    hcc_codes = session.get('hcc_codes', [])
    original_filename = session.get('original_filename', 'Unknown Document')
    
    if not extracted_text:
        flash('No processing results found', 'warning')
        return redirect(url_for('index'))
    
    return render_template(
        'result.html',
        filename=original_filename,
        extracted_text=extracted_text,
        medical_terms=medical_terms,
        hcc_codes=hcc_codes
    )

@app.route('/export', methods=['POST'])
def export_results():
    format_type = request.form.get('format', 'json')
    
    # Get results from session
    extracted_text = session.get('extracted_text', '')
    medical_terms = session.get('medical_terms', [])
    hcc_codes = session.get('hcc_codes', [])
    original_filename = session.get('original_filename', 'Unknown Document')
    
    if not extracted_text:
        return jsonify({'error': 'No results to export'}), 400
    
    export_data = {
        'document_name': original_filename,
        'extracted_text': extracted_text,
        'medical_terms': medical_terms,
        'hcc_codes': hcc_codes
    }
    
    # For now, we only support JSON export
    return jsonify(export_data)

# Error handlers
@app.errorhandler(413)
def too_large(e):
    flash('File too large. Maximum size is 16MB', 'danger')
    return redirect(url_for('index'))

@app.errorhandler(500)
def server_error(e):
    flash('Server error occurred. Please try again later.', 'danger')
    return redirect(url_for('index'))
