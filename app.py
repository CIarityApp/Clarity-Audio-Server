from flask import Flask, request
import os
import clean.py as clean
app = Flask(__name__)

UPLOAD_DESTINATION = 'assets/'
ALLOWED_EXTENSIONS = ['caf', 'mp3', 'mp4', 'wav', 'heic']

app.config['UPLOAD_FOLDER'] = UPLOAD_DESTINATION

msgs = []
new_msgs = []

@app.route('/')
def root():
    return 'Hello, World'

@app.route("/outgoing")
def outgoing():
    return 'Hello, Outgoing'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=['POST'])
def upload_and_clean():
    # Check that file exists
    if 'file' not in request.files:
        return 'File Not Found', 404
    file = request.files['file']

    # Check that filename exists
    if len(file.filename) <= 0:
        return 'Invalid File', 401
    # Check that file is valid
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        clean.clean_audio('/assets/' + file.filename, '/assets/hospital_icu.mp3')
        return '', 201
    else:
        return 'File Not Allowed', 401
    
if __name__ == "__main__":
    app.run(debug=True)