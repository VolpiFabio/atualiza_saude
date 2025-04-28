# arquivo: api_simples.py

from flask import Flask, jsonify, request

app = Flask(__name__)

# Dados simulados
pessoa = {
    "nome": "João",
    "idade": 30
}

# Quando alguém acessar a URL principal
@app.route("/", methods=["GET"])
def home():
    return "API está funcionando!"

# Um "endpoint" que devolve os dados da pessoa
@app.route("/pessoa", methods=["GET"])
def get_pessoa():
    return jsonify(pessoa)

# Um "endpoint" que permite receber um novo nome
@app.route("/pessoa", methods=["POST"])
def criar_pessoa():
    dados = request.get_json()
    pessoa["nome"] = dados.get("nome", pessoa["nome"])
    pessoa["idade"] = dados.get("idade", pessoa["idade"])
    return jsonify({"mensagem": "Pessoa atualizada", "pessoa": pessoa})

# Deixa a API rodando
if __name__ == "__main__":
    app.run(debug=True)
