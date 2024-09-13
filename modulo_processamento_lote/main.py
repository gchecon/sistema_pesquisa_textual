import os
import hashlib
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sqlite3  # Ou psycopg2 para PostgreSQL
from sentence_transformers import SentenceTransformer
import faiss  # Se optar por usar FAISS
# Importar bibliotecas para processamento de cada tipo de arquivo
