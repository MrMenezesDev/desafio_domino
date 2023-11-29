from flask import Flask, request, jsonify
from tipos import Domino
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    data = request.get_json()
    domino = Domino.from_json(data)
    pecas = domino.get_jogadas()
    if pecas is None:
        return jsonify({})
    peca = random.choice(pecas)
    return jsonify(peca.to_dict())

if __name__ == '__main__':
    app.run()
