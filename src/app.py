import os
from flask import Flask, request, render_template, send_file, flash
from werkzeug.utils import secure_filename
from utils.converter import STLto3MFConverter

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Configure upload settings
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
TEMP_FOLDER = os.environ.get('TEMP_FOLDER', 'temp')
ALLOWED_EXTENSIONS = {'stl'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB limit as per PRD

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return render_template('index.html')
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return render_template('index.html')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Ensure directories exist
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            os.makedirs(TEMP_FOLDER, exist_ok=True)
            
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save uploaded file
            file.save(filepath)
            
            try:
                # Convert STL to 3MF
                converter = STLto3MFConverter()
                output_path = converter.convert(filepath)
                
                # Send converted file
                return send_file(
                    output_path,
                    as_attachment=True,
                    download_name=os.path.splitext(filename)[0] + '.3mf',
                    mimetype='application/vnd.ms-package.3dmanufacturing-3dmodel+xml'
                )
            except Exception as e:
                flash(f'Error during conversion: {str(e)}')
                return render_template('index.html')
            finally:
                # Cleanup uploaded file
                if os.path.exists(filepath):
                    os.remove(filepath)
                if 'output_path' in locals() and os.path.exists(output_path):
                    os.remove(output_path)
        
        flash('Invalid file type. Please upload an STL file.')
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 