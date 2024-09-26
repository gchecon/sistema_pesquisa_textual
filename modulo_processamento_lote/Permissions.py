import os
from dotenv import load_dotenv
import getpass


load_dotenv()
EMBEDDINGS_PATH = os.getenv('EMBEDDINGS_PATH', './embeddings')

print(f"Usuário que está rodando o script: {getpass.getuser()}")

# Verificar permissões do diretório de embeddings
print(f"Permissões do diretório {EMBEDDINGS_PATH}: {os.stat(EMBEDDINGS_PATH)}")

test_path = os.path.join(EMBEDDINGS_PATH, 'test.txt')
try:
    with open(test_path, 'w') as f:
        f.write("Teste de permissão de escrita.")
    print(f"Arquivo de teste criado em {test_path}")
except Exception as e:
    print(f"Erro ao criar arquivo de teste: {e}")
