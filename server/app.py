from flask import Flask, request
import clean-audio.py

app = Flask(__name__)

msgs = []
new_msgs = []

@app.route("/outgoing")
def outgoing():
    # return something

@app.route("/incoming", methods=['POST'])
def incoming():


    #input_addy, bg_addy = request.get_something

    final_addy = clean-audio.clean_audio(input_addy, bg_addy)


    new_msgs.append(final_addy)
    return '', 204

    
if __name__ == "__main__":
    app.run(debug=True)