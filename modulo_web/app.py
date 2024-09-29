
from flask import Flask, render_template, request, jsonify
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json
from dotenv import load_dotenv
import os


load_dotenv()
EMBEDDINGS_PATH = os.getenv('EMBEDDINGS_PATH', './embeddings')
MODEL = os.getenv('MODEL_EMBEDDING')

app = Flask(__name__)

# Carregar o modelo de embeddings e o índice FAISS
model = SentenceTransformer(MODEL)
index = faiss.read_index(EMBEDDINGS_PATH)

# Função para buscar os k vetores mais próximos no FAISS
def search_faiss(embedding, top_k=5):
    D, I = index.search(embedding.reshape(1, -1), top_k)
    return I, D

# Endpoint para carregar a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint para processar prompts (futuro)
@app.route('/process_prompt', methods=['POST'])
def process_prompt():

    try:
        data = request.json

        prompt = data.get("prompt")
        if not prompt:
            return jsonify({"error": "Prompt não fornecido"}), 400

        # Gerar o embedding do prompt
        prompt_embedding = model.encode(prompt)

        # Pesquisar no FAISS os vetores mais próximos (retorna os índices e as distâncias)
        indices, distances = search_faiss(prompt_embedding)

        # Recupere os arquivos correspondentes aos índices retornados
        retrieved_documents = []
        for idx in indices[0]:
            # Aqui você precisaria de uma forma de associar o índice com o documento armazenado
            # Exemplo: document_path = recuperar_documento(idx)
            document_text = "Texto de exemplo do documento recuperado"
            retrieved_documents.append(document_text)

        # Concatenar ou formatar os textos recuperados como contexto
        context = "\n".join(retrieved_documents)

        # Geração da resposta pelo LLaMA 3 com base no contexto (aqui você chamaria o modelo local LLaMA 3)
        generated_response = "Aqui seria a resposta gerada pelo LLaMA 3"  # Substitua pela chamada real ao modelo LLaMA 3

        # Retornar a resposta gerada
        return jsonify({"response": generated_response, "context": context})

    except Exception as e:
        print(f"Erro ao processar o prompt: {e}")
        return jsonify({"error": "Erro ao processar o prompt"}), 500


if __name__ == '__main__':
    app.run(debug=True)
