from flask import Flask, request, jsonify
from estrategia import cola_pedra_maior
from tipos import Domino

app = Flask(__name__)

@app.route('/')
def hello_world():
    data = request.get_json()
    domino = Domino.from_json(data)
    return jsonify(cola_pedra_maior(domino).to_dict())

if __name__ == '__main__':
    app.run()
