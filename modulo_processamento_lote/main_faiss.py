import hashlib
import os
import psycopg2
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
import faiss
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import tkinter as tk
from tkinter import simpledialog

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from extratores.docx import extract_text_docx
from extratores.md import extract_text_md
from extratores.odt import extract_text_odt
from extratores.pdf import extract_text_pdf

load_dotenv()
DOCUMENTS_PATH = os.getenv('DOCUMENTS_PATH', './documents')
EMBEDDINGS_PATH = os.getenv('EMBEDDINGS_PATH', './embeddings')
THREADS_COUNT = int(os.getenv('THREADS_COUNT', '4'))
POSTGRESQL_URL = os.getenv('POSTGRESQL_URL')


def store_embedding(file_path, embedding):
    dimension = embedding.shape[0]
    if not os.path.exists(EMBEDDINGS_PATH):
        try:
            os.makedirs(EMBEDDINGS_PATH)
            print(f"Diretório criado: {EMBEDDINGS_PATH}")
        except Exception as e:
            print(f"Erro ao criar diretório {EMBEDDINGS_PATH}: {e}")
            return

    index_path = os.path.join(EMBEDDINGS_PATH, 'embeddings.index')

    try:
        if os.path.exists(index_path):
            index = faiss.read_index(index_path)
            print(f"Índice existente carregado de {index_path}")
        else:
            index = faiss.IndexFlatL2(dimension)
            print(f"Novo índice criado com dimensão {dimension}")

        index.add(embedding.reshape(1, -1))

        try:
            faiss.write_index(index, index_path)
            print(f"Índice salvo em {index_path}")
        except Exception as e:
            print(f"Erro ao escrever o índice em {index_path}: {e}")
            print(f"Permissões do diretório: {os.stat(EMBEDDINGS_PATH)}")

    except Exception as e:
        print(f"Erro ao manipular o índice FAISS: {e}")

    update_processed_files(file_path)


def initialize_faiss():
    if not os.path.exists(EMBEDDINGS_PATH):
        try:
            os.makedirs(EMBEDDINGS_PATH)
            print(f"Diretório de embeddings criado: {EMBEDDINGS_PATH}")
        except Exception as e:
            print(f"Erro ao criar diretório de embeddings {EMBEDDINGS_PATH}: {e}")
            return False

    index_path = os.path.join(EMBEDDINGS_PATH, 'embeddings.index')

    if not os.path.exists(index_path):
        try:
            dimension = model.get_sentence_embedding_dimension()
            index = faiss.IndexFlatL2(dimension)
            faiss.write_index(index, index_path)
            print(f"Novo índice FAISS criado e salvo em {index_path}")
        except Exception as e:
            print(f"Erro ao criar e salvar o índice FAISS inicial: {e}")
            return False

    print(f"FAISS inicializado com sucesso. Arquivo de índice: {index_path}")
    return True

def get_db_connection():
    if POSTGRESQL_URL:
        return psycopg2.connect(POSTGRESQL_URL)
    else:
        root = tk.Tk()
        root.withdraw()
        password = simpledialog.askstring("Password", "Enter database password:", show='*')
        return psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password=password
        )

def extract_text(file_path):
    ext = Path(file_path).suffix.lower()
    if ext == '.pdf':
        return extract_text_pdf(file_path)
    elif ext == '.docx':
        return extract_text_docx(file_path)
    elif ext == '.odt':
        return extract_text_odt(file_path)
    elif ext == '.md':
        return extract_text_md(file_path)
    else:
        print(f'Formato não suportado: {ext}')
        return None

def generate_embedding(text):
    embedding = model.encode(text)
    return embedding

def store_embedding(file_path, embedding):
    dimension = embedding.shape[0]
    if not os.path.exists(EMBEDDINGS_PATH):
        os.makedirs(EMBEDDINGS_PATH)
    index_path = os.path.join(EMBEDDINGS_PATH, 'embeddings.index')

    if os.path.exists(index_path):
        index = faiss.read_index(index_path)
    else:
        index = faiss.IndexFlatL2(dimension)

    index.add(embedding.reshape(1, -1))

    if embedding.shape[0] == dimension:
        faiss.write_index(index, index_path)
    else:
        print(f"Dimensão do embedding ({embedding.shape[0]}) não corresponde ao esperado ({dimension})")

    update_processed_files(file_path)

def process_file(file_path):
    try:
        if is_duplicate(file_path):
            print(f'{file_path} já foi processado.')
            return
        text = extract_text(file_path)
        if text:
            embedding = generate_embedding(text)
            store_embedding(file_path, embedding)
            print(f'Arquivo processado: {file_path}')
        else:
            print(f'Não foi possível extrair texto de {file_path}.')
    except Exception as e:
        print(f'Erro ao processar {file_path}: {e}')

def calculate_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def is_duplicate(file_path):
    file_hash = calculate_file_hash(file_path)
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT 1 FROM files_processed WHERE file_hash = %s', (file_hash,))
            return cur.fetchone() is not None

def update_processed_files(file_path):
    file_hash = calculate_file_hash(file_path)
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO files_processed (file_path, file_hash) VALUES (%s, %s) ON CONFLICT (file_path) DO NOTHING',
                (file_path, file_hash)
            )
        conn.commit()

def scan_and_process():
    files = []
    for root, dirs, filenames in os.walk(DOCUMENTS_PATH):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append(file_path)
    with ThreadPoolExecutor(max_workers=THREADS_COUNT) as executor:
        executor.map(process_file, files)

if __name__ == '__main__':
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Inicialize o FAISS antes de começar o processamento
    initialize_faiss()

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS files_processed (
                    id SERIAL PRIMARY KEY,
                    file_path TEXT UNIQUE,
                    file_hash TEXT,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        conn.commit()

    scan_and_process()