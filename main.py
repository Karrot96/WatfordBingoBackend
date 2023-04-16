import os
import random

from flask import Flask, jsonify, request
from datetime import date
from backend.watford_occurances import watford_occurances
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def generate_card(guid):
    all_cards = watford_occurances[:]
    seed = f"{date.today()}-{guid}"
    random.Random(seed).shuffle(all_cards)
    lists = []
    for i in range(5):
        lists.append(all_cards[i * 5 : i * 5 + 5])
    return lists


@app.route("/generate", methods=["POST"])
def generate():
    guid = request.get_json().get("guid")
    if not guid:
        return jsonify({"error": "Missing GUID"}), 400
    card = generate_card(guid)
    return jsonify(card)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
