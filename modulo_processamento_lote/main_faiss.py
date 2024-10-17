import hashlib
import os
import psycopg2
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
import faiss
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import tkinter as tk
from tkinter import simpledialog
import logging

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
MODEL = os.getenv('MODEL_EMBEDDING')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'ERROR').upper()

logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)


def initialize_faiss():
    if not os.path.exists(EMBEDDINGS_PATH):
        os.makedirs(EMBEDDINGS_PATH)
        print(f"Diretório de embeddings criado: {EMBEDDINGS_PATH}")

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


def generate_embedding(text):
    return model.encode(text)


def store_embedding(file_path, embedding):
    index_path = os.path.join(EMBEDDINGS_PATH, 'embeddings.index')
    index = faiss.read_index(index_path)
    index.add(embedding.reshape(1, -1))
    faiss.write_index(index, index_path)

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


def get_db_connection():
    logger.debug("Tentando estabelecer conexão com o banco de dados")
    if POSTGRESQL_URL:
        conn = psycopg2.connect(POSTGRESQL_URL)
        logger.debug("Conexão estabelecida com sucesso")
        return conn
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
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        print(f'Formato não suportado: {ext}')
        return None


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
    model = SentenceTransformer(MODEL)

    # Inicialize o FAISS antes de começar o processamento
    if not initialize_faiss():
        print("Falha na inicialização do FAISS. O programa será encerrado.")
        sys.exit(1)

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