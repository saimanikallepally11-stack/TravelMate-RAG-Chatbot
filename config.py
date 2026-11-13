import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
DATA_DIR = "data"
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "telangana_tourism_knowledge"
CHUNK_SIZE = 900
CHUNK_OVERLAP = 150
TOP_K = 4
