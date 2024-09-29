
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Endpoint para carregar a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint para processar prompts (futuro)
@app.route('/process_prompt', methods=['POST'])
def process_prompt():
    data = request.json
    # Aqui você pode adicionar a lógica para aproximar vetores e gerar resposta usando o modelo RAG.
    return jsonify({"response": "Resposta gerada será inserida aqui"})

if __name__ == '__main__':
    app.run(debug=True)
