import aiml, os
from flask import Flask, render_template, request, jsonify
from auto_correct import correction
from flask_cors import CORS, cross_origin

# creating kernel and learning AIML files
kernel = aiml.Kernel()

# Faster if bootstrap already exists
if os.path.isfile("maleo_brain.brn"):
    kernel.bootstrap(brainFile="maleo_brain.brn")
else:
    kernel.bootstrap(learnFiles="start.xml", commands="CAFE")
    kernel.saveBrain("maleo_brain.brn")

def get_respond_from_backend(msg):
    print(f"Input message: {msg}")
    response = kernel.respond(msg)
    print(f"Kernel response: {response}")
    
    if response:
        return response
    else:
        msg = msg+"ya"
        response = kernel.respond(msg)
        print(f"Kernel response: {response}")

        if response:
            return response
        else:
            msg = "ya "+msg+"ya"
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
    msgCorrect = ""
    arrayMsg = msg.split(" ")
    for kata in arrayMsg:
        msgCorrect += correction(kata) + " "
    print("Hasil Koreksi : " + msgCorrect)

    respond = get_respond_from_backend(msgCorrect).split(" ")
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