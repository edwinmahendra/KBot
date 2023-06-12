import random
import aiml
import os

import re
from collections import Counter

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


class Bot:
    def __init__(self, aiml_kernel=None):
        self.kernel = aiml_kernel if aiml_kernel else aiml.Kernel()
        self._learn_aiml()
        self.unknown_responses = [
            "Mohon maaf, saya tidak memahami pesan anda.",
            "Maaf, saya tidak mengerti apa yang Anda maksud.",
            "Saya tidak yakin apa yang Anda coba katakan. Bisakah Anda ulangi?",
            "Maaf, saya masih belajar. Bisakah Anda menggambarkan itu dengan cara lain?",
        ]
        self.menu_not_found_responses = [
            "Maaf, menu {} tidak ada di menu kami.",
            "Mohon maaf, kami tidak menyediakan menu {}.",
            "Menu {}? Maaf, itu tidak tersedia di menu kami."
        ]

    def _learn_aiml(self):
        self.kernel.learn("start.xml")
        self.kernel.respond("KFC")
        self.kernel.saveBrain("kbot.bot")

    def get_response(self, pesan):
        response = self.kernel.respond(pesan)
        if response == "unknown_menu":
            menu_item = re.search(r'menu ([a-zA-Z0-9_-]+)', pesan)
            unknown_item = re.search(r'apa itu ([a-zA-Z0-9_-]+)', pesan)
            apa_sih_item = re.search(r'apa sih ([a-zA-Z0-9_-]+)', pesan)
            if menu_item:
                return random.choice(self.menu_not_found_responses).format(menu_item.group(1))
            elif unknown_item:
                return random.choice(self.menu_not_found_responses).format(unknown_item.group(1))
            elif apa_sih_item:
                return random.choice(self.menu_not_found_responses).format(apa_sih_item.group(1).split(' itu')[0])            
            # if menu_item:
            #     #berapa harga / adakah menu lotek then system will print maaf, menu {lotek} tidak ada di menu kami
            #     return random.choice(self.menu_not_found_responses).format(menu_item.group(1))
            # elif unknown_item:
            #     return random.choice(self.menu_not_found_responses).format(unknown_item.group(1))
            # else:
            #     return "Maaf, saya tidak menemukan menu yang Anda tanyakan."
        else:
            return response if response else random.choice(self.unknown_responses)
    
class TextCorrection:
    def __init__(self, corpus):
         # The constructor that initializes a Counter with words from the given corpus.
        self.words_counter = Counter(self.extract_words(open(corpus).read()))

    def extract_words(self, text):
        # This function extracts all the words from the given text using regex.
        return re.findall(r'\w+', text.lower())

    def probability(self, word, total=None):
        # This function calculates the probability of the given word by dividing the count of the word
        # by the total number of words. If total is not given, it calculates the total.
        total = total if total else sum(self.words_counter.values())
        return self.words_counter[word] / total

    def correct_word(self, word):
        # This function corrects a given word by choosing the most probable word from its possible corrections.
        return max(self.possible_corrections(word), key=self.probability)

    def possible_corrections(self, word):
        # This function returns the possible corrections for a given word. The corrections can be a known word,
        # words at an edit distance of 1, words at an edit distance of 2, or the word itself.
        return (self.known([word]) or self.known(self.edit_distance_1(word)) 
                or self.known(self.edit_distance_2(word)) or [word])

    def known(self, words):
        # This function returns the words that are known, i.e., the words that exist in the word counter.
        return set(w for w in words if w in self.words_counter)

    def edit_distance_1(self, word):
        # This function returns the words that are at an edit distance of 1 from the given word.
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [self.delete_letter(L, R) for L, R in splits if R]
        transposes = [self.transpose_letters(L, R) for L, R in splits if len(R)>1]
        replaces   = [self.replace_letter(L, R, c) for L, R in splits if R for c in letters]
        inserts    = [self.insert_letter(L, R, c) for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edit_distance_2(self, word):
        # This function returns the words that are at an edit distance of 2 from the given word.
        return (e2 for e1 in self.edit_distance_1(word) for e2 in self.edit_distance_1(e1))

    def delete_letter(self, left, right):
        # This function deletes a letter from a word, given the left and right parts of the word.
        return left + right[1:]

    def transpose_letters(self, left, right):
        # This function transposes two letters of a word, given the left and right parts of the word.
        return left + right[1] + right[0] + right[2:]

    def replace_letter(self, left, right, c):
        # This function replaces a letter of a word with a given character, given the left and right parts of the word.
        return left + c + right[1:]

    def insert_letter(self, left, right, c):
        # This function inserts a given character into a word, given the left and right parts of the word.
        return left + c + right

def create_app():
    app = Flask(__name__)
    CORS(app)
    bot = Bot()
    text_correction = TextCorrection('corpus.txt')

    @app.route("/")
    def home():
        return render_template("base.html")

    @app.route("/predict", methods=['POST'])
    def send_message():
        pesan = request.get_json()["message"]
        print(pesan)
        
        # Correct each word in the message
        pesanFix = " ".join(text_correction.correct_word(word) for word in pesan.split())
        print("User Chat    : " + pesanFix)

        # Get bot's response and split it into words
        response_words = bot.get_response(pesanFix).split()

        # Substitute "^" with "<br>" in the response
        response_bot = " ".join("<br>" if word == "^" else word for word in response_words)
        print("Bot      : " + response_bot)

        # Return the corrected response
        return jsonify({"message": response_bot.strip()})

    return app

if __name__ == "__main__":
    create_app().run(debug=True, port=5001)