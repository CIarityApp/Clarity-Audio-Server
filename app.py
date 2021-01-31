from flask import Flask, request
import clean-audio.py
app = Flask(__name__)

UPLOAD_DESTINATION = 'assets/'

msgs = []
new_msgs = []

@app.route('/')
def root():
    return 'Hello, World'

@app.route("/outgoing")
def outgoing():
    return 'Hello, Outgoing'

@app.route("/incoming", methods=['POST'])
def incoming():
    final_addy = clean-audio.clean_audio(input_addy, bg_addy)

    new_msgs.append(final_addy)
    return '', 204
    
if __name__ == "__main__":
    app.run(debug=True)