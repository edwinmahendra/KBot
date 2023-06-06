import aiml, os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin

# creating kernel and learning AIML files
kernel = aiml.Kernel()

# Faster if bootstrap already exists
if os.path.isfile("kbot.brn"):
    kernel.bootstrap(brainFile="kbot.brn")
else:
    kernel.bootstrap(learnFiles="start.xml", commands="KFC")
    kernel.saveBrain("kbot.brn")

def get_respond_from_backend(msg):
    print(f"Input message: {msg}")
    response = kernel.respond(msg)
    print(f"Kernel response: {response}")
    
    if response:
        return response
    else:
        return "Maaf... saya kurang mengerti"

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/predict", methods=['POST'])
@cross_origin() # This will enable CORS for this route
def send_message():
    msg = request.get_json()["message"]
    respond = get_respond_from_backend(msg).split(" ")
    tampungRespond = ""
    for kataRespond in respond:
        if kataRespond == "~":
            tampungRespond += "\n\t   "
            continue
        elif kataRespond == "*":
            tampungRespond += "\t"
            continue
        tampungRespond += kataRespond + " "
    return jsonify({"message": tampungRespond})

if __name__ == "__main__":
    app.run(debug=True, port=5001)