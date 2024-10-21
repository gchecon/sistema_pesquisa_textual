import os
import logging
from llama_cpp import Llama

logging.basicConfig(level=logging.DEBUG)

LLAMA_MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'Llama3.1-70B'))

print(f"Tentando carregar modelo de: {LLAMA_MODEL_PATH}")
print(f"O arquivo existe? {os.path.exists(LLAMA_MODEL_PATH)}")
print(f"Permissões do arquivo: {oct(os.stat(LLAMA_MODEL_PATH).st_mode)[-3:]}")

try:
    llama_model = Llama(model_path=LLAMA_MODEL_PATH, n_gpu_layers=-1, n_ctx=2048, verbose=True)
    print("Modelo carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o modelo: {str(e)}")