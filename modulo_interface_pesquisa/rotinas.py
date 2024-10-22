import faiss
import logging
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
DOCUMENTS_PATH = os.getenv('DOCUMENTS_PATH', './documents')
EMBEDDINGS_PATH = os.getenv('EMBEDDINGS_PATH', './embeddings')
THREADS_COUNT = int(os.getenv('THREADS_COUNT', '4'))
POSTGRESQL_URL = os.getenv('POSTGRESQL_URL')
MODEL = os.getenv('MODEL_EMBEDDING')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'ERROR').upper()

logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)

def get_db_connection():
    logger.debug("Tentando estabelecer conexão com o banco de dados")
    if POSTGRESQL_URL:
        conn = psycopg2.connect(POSTGRESQL_URL)
        logger.debug("Conexão estabelecida com sucesso")
        return conn
    else:
        return 'Não existe informação do Banco de Dados'

def search_similar_documents(query_text, model, top_k=5):
    query_embedding = model.encode(query_text)
    index = faiss.read_index(os.path.join(EMBEDDINGS_PATH, 'embeddings.index'))

    distances, indices = index.search(query_embedding.reshape(1, -1), top_k)

    results = []
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            for i, idx in enumerate(indices[0]):
                embedding_bytes = index.reconstruct(int(idx)).tobytes()
                cur.execute("SELECT file_name FROM files_processed WHERE embedding_id = %s",
                            (psycopg2.Binary(embedding_bytes),))
                result = cur.fetchone()
                if result:
                    results.append((result[0], distances[0][i]))

    return results