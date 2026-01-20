import os
import sqlite3
import bcrypt
from pathlib import Path
from dotenv import load_dotenv

# --- CONFIGURAZIONE AMBIENTE ---
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

# Gestione percorsi Database
RAW_DB_PATH = os.getenv("SQLITE_PATH", "DATABASE.sqlite3")
db_path_obj = Path(RAW_DB_PATH)

if db_path_obj.is_absolute():
    DB_PATH = db_path_obj
else:
    DB_PATH = BASE_DIR / db_path_obj

SCHEMA_PATH = BASE_DIR / "schema.sql"

# --- INIZIALIZZAZIONE ---

def _init_db():
    """Inizializza il database applicando lo schema SQL."""
    with sqlite3.connect(DB_PATH, timeout=5) as conn:
        schema_content = SCHEMA_PATH.read_text(encoding="utf-8")
        conn.executescript(schema_content)

_init_db()

# --- LOGICA UTENTI ---

def create_user(username, email, password):
    """Crea un nuovo utente con password hashata."""
    # Generazione Hash
    salt = bcrypt.gensalt()
    pwd_hash = bcrypt.hashpw(password.encode(), salt).decode()

    try:
        with sqlite3.connect(DB_PATH, timeout=5) as conn:
            query = "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)"
            conn.execute(query, (username, email, pwd_hash))
        return True
    except sqlite3.IntegrityError:
        # Errore in caso di email o username duplicati
        return False

def authenticate_user(email, password):
    """Verifica le credenziali dell'utente."""
    query = "SELECT password_hash FROM users WHERE email = ?"
    
    with sqlite3.connect(DB_PATH, timeout=5) as conn:
        row = conn.execute(query, (email,)).fetchone()

    if not row:
        return False

    # Verifica hash: password fornita vs hash nel DB
    stored_hash = row[0].encode()
    return bcrypt.checkpw(password.encode(), stored_hash)