import aiml
import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from auto_correct import correction

class Bot:
    def __init__(self, aiml_kernel=None):
        self.kernel = aiml_kernel if aiml_kernel else aiml.Kernel()
        self._learn_aiml()

    def _learn_aiml(self):
        if os.path.isfile("kbot.bot"):
            self.kernel.bootstrap(brainFile="kbot.bot")
        else:
            self.kernel.bootstrap(learnFiles="start.xml", commands="KFC")
            self.kernel.saveBrain("kbot.bot")

    def get_response(self, pesan):
        response = self.kernel.respond(pesan)
        return response if response else "Maaf... saya kurang mengerti"

def create_app():
    app = Flask(__name__)
    CORS(app)
    bot = Bot()

    @app.route("/")
    def home():
        return render_template("base.html")

    @app.route("/predict", methods=['POST'])
    def send_message():
        pesan = request.get_json()["message"]
        print(pesan)
        
        pesanFix = ""
        pesanArray = pesan.split(" ")
        for i in pesanArray:
            pesanFix += correction(i) + " "
            
        print("Hasil Koreksi : " + pesanFix)
        response = bot.get_response(pesanFix)
        
        return jsonify({"message": response})

    return app

if __name__ == "__main__":
    create_app().run(debug=True, port=5001)