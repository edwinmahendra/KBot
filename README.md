# ChatBot with AIML and Text Correction

## 📝  Description
This project is a simple chatbot application that integrates Artificial Intelligence Markup Language (AIML) for generating responses and utilizes a basic text correction functionality to correct the user's input message. It's designed to answer questions related to food ordering, specifically for a restaurant like KFC.

## 👥  Developers
- Edwin Mahendra
- Johannes Baptista Adiatmaja

Since this was made, we are students of Duta Wacana Christian University who have not yet graduated.

## 🚀  How to Use
1. Clone the repository.
2. Install the required libraries as mentioned below.
3. Run the `chatbot_backend.py` file to start the Flask server.
4. Navigate to `localhost:5001` on your browser to access the chatbot UI.
5. You can chat with the bot by typing your questions in the chatbox.

Note: To run this project, Python 3 is required.

## 📚  Imported Libraries
This project uses the following Python libraries:
| Library | Import Code | Install Command |
|---|---|---|
| [`aiml`](https://pypi.org/project/python-aiml/) | `import aiml` | `pip install python-aiml` |
| [`os`](https://docs.python.org/3/library/os.html) | `import os` | (built-in) |
| [`re`](https://docs.python.org/3/library/re.html) | `import re` | (built-in) |
| [`collections`](https://docs.python.org/3/library/collections.html) | `from collections import Counter` | (built-in) |
| [`flask`](https://pypi.org/project/Flask/) | `from flask import Flask, jsonify, request` | `pip install flask` |
| [`flask_cors`](https://pypi.org/project/Flask-Cors/) | `from flask_cors import CORS` | `pip install Flask-Cors` |

## 📢  Feedback
Your feedback is valuable to us in improving this chatbot application. If you have any issues, questions or suggestions, feel free to open an issue on this repository. We will try to address it as soon as possible.

## 🏅  Credit
The text correction algorithm implemented in this project is inspired by Peter Norvig's article ["How to Write a Spelling Corrector"](https://norvig.com/spell-correct.html). Peter Norvig is a Director of Research at Google Inc, and his work in spelling correction and natural language processing has significantly impacted the field. We'd like to express our gratitude for his substantial contribution to the community and for making his knowledge openly available for learning and improvement purposes.

##  ⚠️  Disclaimer

Please note that the content provided here does not originate from KFC or any of its affiliates. The food and drink menu items listed here are inspired by the offerings of KFC Indonesia, and are used purely for illustrative purposes. 

This repository, its author, and contributors are not affiliated, endorsed, or sponsored by KFC, Yum! Brands, or any of their subsidiaries. The information in this repository is provided "as is" without any representations or warranties, express or implied. 

The use of the KFC name and/or its menu offerings does not imply any connection or association with KFC Corporation, Yum! Brands, or any KFC outlets worldwide. The KFC name, logos, and related trademarks are the property of their respective trademark holders.

By using this information, you agree to do so at your own discretion and risk. The author and contributors to this repository shall not be held liable for any damages or any form of loss resulting from the use of this information.
