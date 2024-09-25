import hashlib
import os
import sqlite3  # Ou psycopg2 para PostgreSQL
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
import faiss  # Se optar por usar FAISS
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from extratores.docx import *
from extratores.md import *
from extratores.odt import *
from extratores.pdf import *


load_dotenv()
DOCUMENTS_PATH = os.getenv('DOCUMENTS_PATH', './documents')
PROCESSED_DB_PATH = os.getenv('PROCESSED_DB_PATH', './processed_files.db')
EMBEDDINGS_PATH = os.getenv('EMBEDDINGS_PATH', './embeddings')
THREADS_COUNT = int(os.getenv('THREADS_COUNT', '4'))


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
    # Exemplo usando FAISS
    dimension = embedding.shape[0]
    if not os.path.exists(EMBEDDINGS_PATH):
        os.makedirs(EMBEDDINGS_PATH)
    index_path = os.path.join(EMBEDDINGS_PATH, 'embeddings.index')

    if os.path.exists(index_path):
        index = faiss.read_index(index_path)
    else:
        index = faiss.IndexFlatL2(dimension)

    index.add(embedding.reshape(1, -1))
    faiss.write_index(index, index_path)

    # Atualizar metadados
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
    cursor.execute('SELECT 1 FROM files_processed WHERE file_hash = ?', (file_hash,))
    return cursor.fetchone() is not None


def update_processed_files(file_path):
    file_hash = calculate_file_hash(file_path)
    cursor.execute('INSERT OR IGNORE INTO files_processed (file_path, file_hash) VALUES (?, ?)', (file_path, file_hash))
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
    # Carregar o modelo uma única vez
    model = SentenceTransformer('all-MiniLM-L6-v2')

    conn = sqlite3.connect(PROCESSED_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files_processed (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT UNIQUE,
            file_hash TEXT,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

    scan_and_process()
    conn.close()
