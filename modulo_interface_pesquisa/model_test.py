import os
import logging
from llama_cpp import Llama
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'ERROR').upper()

logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)

#LLAMA_MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'Llama3.1-70B'))
LLAMA_MODEL_PATH = os.getenv('LLAMA_MODEL_PATH')

if not os.path.exists(LLAMA_MODEL_PATH):
    raise FileNotFoundError(f"Modelo de LLama não encontrado em: {LLAMA_MODEL_PATH}")

if not os.access(LLAMA_MODEL_PATH, os.R_OK):
    raise PermissionError(f"Permissão insuficiente para ler o modelo em: {LLAMA_MODEL_PATH}")

print(f"Tentando carregar modelo de: {LLAMA_MODEL_PATH}")
print(f"O arquivo existe? {os.path.exists(LLAMA_MODEL_PATH)}")
print(f"Permissões do arquivo: {oct(os.stat(LLAMA_MODEL_PATH).st_mode)[-3:]}")

try:
    llama_model = Llama(model_path=LLAMA_MODEL_PATH, n_gpu_layers=0, n_ctx=2048, verbose=True)
    print("Modelo carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o modelo: {str(e)}")