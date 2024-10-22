from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os
import logging

load_dotenv()

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'ERROR').upper()

logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)

#LLAMA_MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'Llama3.1-70B'))
LLAMA_MODEL_PATH = os.getenv('LLAMA_MODEL_PATH')

chat_model = ChatOllama(model=LLAMA_MODEL_PATH)
response = chat_model.invoke("Quem foi o primeiro homem a pisar na lua?")
print(response)
