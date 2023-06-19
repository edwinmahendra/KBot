import random
import aiml

import re
from collections import Counter

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

class Bot:
    def __init__(self, aiml_kernel = None):
        self.kernel = aiml_kernel if aiml_kernel else aiml.Kernel()
        self._learn_aiml()
        self.unknown_responses = [
            "Mohon maaf, saya tidak memahami pesan anda.",
            "Maaf, saya tidak mengerti apa yang Anda maksud.",
            "Saya tidak yakin apa yang Anda coba katakan. Bisakah Anda ulangi?",
            "Maaf, saya masih belajar. Bisakah Anda menggambarkan itu dengan cara lain?",
            "Sepertinya saya tidak dapat memahami. Bisakah Anda coba mengatakannya lagi?",
            "Mohon maaf, saya masih belajar dan belum mengerti itu. Bisa tolong jelaskan lagi?",
            "Saya minta maaf atas ketidaknyamanannya. Bisakah Anda ulangi atau jelaskan dengan lebih detail?",
            "Maaf, saya belum bisa memahami itu sepenuhnya. Bisa ulangi lagi?",
            "Saya belum bisa memahami maksud Anda. Bisakah Anda memberikan lebih banyak detail?",
            "Maaf, saya belum bisa memproses pertanyaan Anda. Bisa tolong jelaskan lagi?",
            "Maaf, saya belum mengerti. Bisa tolong ulangi lagi dengan lebih jelas?",
            "Saya minta maaf, saya belum sepenuhnya mengerti. Bisa Anda jelaskan dengan cara lain?",
            "Saya belum memahami maksud Anda. Bisakah Anda mengulasnya lagi?",
            "Maaf, saya belum sepenuhnya mengerti pertanyaan Anda. Bisa Anda ulangi atau jelaskan lebih lanjut?",
        ]
        self.menu_not_found_responses = [
            "Maaf, menu {} tidak ada di menu kami.",
            "Mohon maaf, kami tidak menyediakan menu {}.",
            "Menu {}? Maaf, itu tidak tersedia di menu kami.",
            "Maaf, {} tidak ada di dalam daftar menu kami."
        ]

    def _learn_aiml(self):
        self.kernel.learn("start.xml")
        self.kernel.respond("KFC")
        self.kernel.saveBrain("kbot.brn")

    def get_response(self, pesan):
        response = self.kernel.respond(pesan)
        if response == "unknown_menu":
            patterns = [
                (r'menu (.+)', self.menu_not_found_responses),
                (r'apa itu (.+)', self.menu_not_found_responses),
                (r'apa sih (.+)', self.menu_not_found_responses),
                (r'bagaimana dengan menu (.+)', self.menu_not_found_responses),
                (r'apa yang anda tahu tentang (.+)', self.menu_not_found_responses),
                (r'bisakah anda memberi tahu saya tentang (.+)', self.menu_not_found_responses),
                (r'berapa harga (.+)', self.menu_not_found_responses)
            ]

            for pattern, response_list in patterns:
                match = re.search(pattern, pesan)
                if match:
                    item = match.group(1)
                    # Jika pesan diakhiri dengan ' itu', hapus item tersebut dari item
                    if item.endswith(' itu'):
                        item = item[:-4]
                    return random.choice(response_list).format(item)
            
        else:
            return response if response else random.choice(self.unknown_responses)
    
class TextCorrection:
    def __init__(self, corpus):
        # Konstruktor yang menginisialisasi Counter dengan kata-kata dari korpus yang diberikan.
        self.words_counter = Counter(self.extract_words(open(corpus).read()))

    def extract_words(self, text):
        # Fungsi ini mengekstrak semua kata dari teks yang diberikan menggunakan regex.
        return re.findall(r'\w+', text.lower())

    def probability(self, word, total=None):
        # Fungsi ini menghitung probabilitas kata yang diberikan dengan membagi jumlah kata dengan jumlah total kata
        total = total if total else sum(self.words_counter.values())
        return self.words_counter[word] / total

    def correct_word(self, word):
        # Fungsi ini mengoreksi kata yang diberikan dengan memilih kata yang paling mungkin dari kemungkinan koreksinya.
        return max(self.possible_corrections(word), key=self.probability)

    def possible_corrections(self, word):
        # Fungsi ini mengembalikan koreksi yang mungkin untuk kata yang diberikan. Koreksi dapat berupa kata yang sudah diketahui,
        # kata dengan jarak edit 1, kata dengan jarak edit 2, atau kata itu sendiri.
        return (self.known([word]) or self.known(self.edit_distance_1(word)) 
                or self.known(self.edit_distance_2(word)) or [word])

    def known(self, words):
        # Fungsi ini mengembalikan kata-kata yang diketahui, yaitu kata-kata yang ada dalam penghitung kata.
        return set(w for w in words if w in self.words_counter)

    def edit_distance_1(self, word):
        # Fungsi ini mengembalikan kata-kata yang berada pada jarak edit 1 dari kata yang diberikan.
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [self.delete_letter(L, R) for L, R in splits if R]
        transposes = [self.transpose_letters(L, R) for L, R in splits if len(R)>1]
        replaces   = [self.replace_letter(L, R, c) for L, R in splits if R for c in letters]
        inserts    = [self.insert_letter(L, R, c) for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edit_distance_2(self, word):
        # Fungsi ini mengembalikan kata-kata yang berada pada jarak edit 2 dari kata yang diberikan.
        return (e2 for e1 in self.edit_distance_1(word) for e2 in self.edit_distance_1(e1))

    def delete_letter(self, left, right):
        # Fungsi ini menghapus huruf dari sebuah kata, dengan memperhatikan bagian kiri dan kanan kata tersebut.
        return left + right[1:]

    def transpose_letters(self, left, right):
        # Fungsi ini mentransposisikan dua huruf dari sebuah kata, dengan memberikan bagian kiri dan kanan dari kata tersebut.
        return left + right[1] + right[0] + right[2:]

    def replace_letter(self, left, right, c):
        # Fungsi ini menggantikan huruf dari sebuah kata dengan karakter tertentu, yang diberikan pada bagian kiri dan kanan kata tersebut.
        return left + c + right[1:]

    def insert_letter(self, left, right, c):
        # Fungsi ini menyisipkan karakter tertentu ke dalam sebuah kata, dengan memperhatikan bagian kiri dan kanan kata tersebut.
        return left + c + right
    
def remove_trailing_punctuation(text):
    pattern = r'[^\w\s]*$'
    return re.sub(pattern, '', text)

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
        
        pesan = remove_trailing_punctuation(pesan)
        print('\nRevisi Pesan: ' + pesan +'\n')
        
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