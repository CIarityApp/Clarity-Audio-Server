from flask import Flask, request
import os

import firebase_admin
from firebase import firebase
from firebase_admin import credentials, firestore, initialize_app, storage, db

import clean
app = Flask(__name__)

MY_DIR = os.path.dirname(__file__)
UPLOAD_DESTINATION = 'tmp/'
ALLOWED_EXTENSIONS = ['caf', 'mp3', 'mp4', 'wav', 'heic']

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, { 'storageBucket': 'clarity-81765.appspot.com' })
realtime = firebase.FirebaseApplication('https://clarity-81765-default-rtdb.firebaseio.com/', None)
# realtime = db.ref('clarity-81765-default-rtdb')
bucket = storage.bucket()

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
        file.save(os.path.join(MY_DIR, file.filename))
        file_loc = MY_DIR + '/' + file.filename
        # final_file_addr = clean.clean_audio(file_loc, MY_DIR + '/assets/hospital_icu.mp3')
        
        # Upload to firebase
        blob = bucket.blob('actual.caf')
        blob.upload_from_filename(file_loc)
        blob.make_public()

        info = realtime.post('files', { "next": 'actual.caf' })

        return info, 201
    else:
        return 'File Not Allowed', 401
    
if __name__ == "__main__":
    app.run(debug=True)