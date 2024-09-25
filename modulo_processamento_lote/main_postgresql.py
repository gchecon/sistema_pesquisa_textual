import hashlib
import os
import psycopg2
from psycopg2.extensions import register_adapter, AsIs
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
import numpy as np
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
POSTGRESQL_URL = os.getenv('POSTGRESQL_URL')
THREADS_COUNT = int(os.getenv('THREADS_COUNT', '4'))
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '500'))


# Adaptar numpy array para PostgreSQL
def addapt_numpy_array(numpy_array):
    return AsIs(f"ARRAY{numpy_array.tolist()}")

def addapt_numpy_float32(numpy_float32):
    return AsIs(numpy_float32)

register_adapter(np.float32, addapt_numpy_float32)
register_adapter(np.ndarray, addapt_numpy_array)


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


def generate_embeddings(text):
    # Divide o texto em chunks
    chunks = [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
    embeddings = model.encode(chunks)
    return embeddings


def store_embeddings(file_path, embeddings):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                for i, embedding in enumerate(embeddings):
                    cur.execute("""
                        INSERT INTO document_embeddings (file_path, chunk_index, embedding)
                        VALUES (%s, %s, %s::float4[])
                        ON CONFLICT (file_path, chunk_index) DO UPDATE
                        SET embedding = EXCLUDED.embedding
                    """, (file_path, i, embedding))
                conn.commit()
                print(f"Embeddings armazenados com sucesso para {file_path}")
            except Exception as e:
                print(f"Erro ao armazenar embeddings para {file_path}: {e}")
                print(f"Embedding causador do erro: {embedding}")
                print(f"SQL gerado: {cur.mogrify('INSERT INTO document_embeddings (file_path, chunk_index, embedding) VALUES (%s, %s, %s::float4[])', (file_path, i, embedding))}")
                conn.rollback()


def process_file(file_path):
    try:
        if is_duplicate(file_path):
            print(f'{file_path} já foi processado.')
            return
        text = extract_text(file_path)
        if text:
            embeddings = generate_embeddings(text)
            store_embeddings(file_path, embeddings)
            update_processed_files(file_path)
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


def initialize_database():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Criar extensão vector se não existir
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

            # Criar tabela para embeddings
            cur.execute("""
                CREATE TABLE IF NOT EXISTS document_embeddings (
                    id SERIAL PRIMARY KEY,
                    file_path TEXT,
                    chunk_index INTEGER,
                    embedding vector(384),
                    UNIQUE(file_path, chunk_index)
                )
            """)

            # Criar tabela para arquivos processados
            cur.execute("""
                CREATE TABLE IF NOT EXISTS files_processed (
                    id SERIAL PRIMARY KEY,
                    file_path TEXT UNIQUE,
                    file_hash TEXT,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Criar índice para busca por similaridade
            cur.execute("""
                CREATE INDEX IF NOT EXISTS embedding_index 
                ON document_embeddings 
                USING ivfflat (embedding vector_cosine_ops)
                WITH (lists = 100)
            """)
        conn.commit()


if __name__ == '__main__':
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Inicializar o banco de dados
    initialize_database()

    scan_and_process()