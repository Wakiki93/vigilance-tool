"""
Web interface for the API Breaking Change Risk Vigilance Tool.
Provides a user-friendly interface for product managers and non-technical users.
"""
import os
import sys
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, flash, redirect, url_for

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.loader import load_openapi_spec
from src.differ import compare_specs
from src.scorer import (
    calculate_raw_score,
    normalize_to_1_10_scale,
    determine_risk_level_and_action
)

app = Flask(__name__)
app.secret_key = 'vigilance-tool-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'yaml', 'yml', 'json'}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render the main upload page."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle file upload and perform analysis."""
    # Check if files were uploaded
    if 'old_spec' not in request.files or 'new_spec' not in request.files:
        flash('Please upload both specification files', 'error')
        return redirect(url_for('index'))

    old_file = request.files['old_spec']
    new_file = request.files['new_spec']

    # Check if files are selected
    if old_file.filename == '' or new_file.filename == '':
        flash('Please select both files', 'error')
        return redirect(url_for('index'))

    # Validate file extensions
    if not (allowed_file(old_file.filename) and allowed_file(new_file.filename)):
        flash('Invalid file type. Please upload YAML or JSON files', 'error')
        return redirect(url_for('index'))

    # Save files temporarily
    old_filename = secure_filename(old_file.filename)
    new_filename = secure_filename(new_file.filename)

    old_path = os.path.join(app.config['UPLOAD_FOLDER'], 'old_' + old_filename)
    new_path = os.path.join(app.config['UPLOAD_FOLDER'], 'new_' + new_filename)

    old_file.save(old_path)
    new_file.save(new_path)

    try:
        # Load specifications
        old_spec = load_openapi_spec(old_path)
        new_spec = load_openapi_spec(new_path)

        if not old_spec or not new_spec:
            flash('Failed to parse specification files', 'error')
            return redirect(url_for('index'))

        # Perform analysis
        diff_result = compare_specs(old_spec, new_spec)
        raw_score = calculate_raw_score(diff_result)
        risk_score = normalize_to_1_10_scale(raw_score)
        risk_info = determine_risk_level_and_action(risk_score)

        # Get differences list
        differences = diff_result.get('differences', [])

        # Render results
        return render_template(
            'results.html',
            risk_score=risk_score,
            risk_info=risk_info,
            differences=differences,
            old_filename=old_filename,
            new_filename=new_filename
        )

    except Exception as e:
        flash(f'Error analyzing files: {str(e)}', 'error')
        return redirect(url_for('index'))

    finally:
        # Clean up uploaded files
        if os.path.exists(old_path):
            os.remove(old_path)
        if os.path.exists(new_path):
            os.remove(new_path)


if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
