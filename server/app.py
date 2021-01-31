from flask import Flask, request

app = Flask(__name__)

msgs = []
new_msgs = []

@app.route("/outgoing")
def outgoing():
    # return something

@app.route("/incoming", methods=['POST'])
def incoming():
    # msgs.append(request.get_something)
    return '', 204

    
if __name__ == "__main__":
    app.run(debug=True)