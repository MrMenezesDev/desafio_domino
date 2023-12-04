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
    peca_maior = None
    peca_menor = None
    for peca in pecas:
        peca_maior = peca if peca_maior is None or peca_maior.get_tamanho() > peca.peca.get_tamanho() else peca_maior
        peca_menor =  peca if peca_menor is None or peca_menor.get_tamanho() < peca.peca.get_tamanho() else peca_menor

    epeca = peca_maior if domino.jogador % 2 == 0 else peca_menor
    rpeca = random.choice(pecas)
    peca = epeca if random.randint(1, 100) <= 20 else rpeca
    return jsonify(peca.to_dict())

if __name__ == '__main__':
    app.run()
