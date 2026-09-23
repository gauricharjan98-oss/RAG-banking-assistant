
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
POLICIES_DIR = DATA_DIR / "policies"
EVAL_DIR = DATA_DIR / "eval"

# Local database and vector store
DATABASE_PATH = DATA_DIR / "novabank.db"
CHROMA_PATH = DATA_DIR / "chroma_db"

# Create required data directories if missing
POLICIES_DIR.mkdir(parents=True, exist_ok=True)
EVAL_DIR.mkdir(parents=True, exist_ok=True)