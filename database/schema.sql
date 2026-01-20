-- Tabella utenti condivisa da Flask ed Express.
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL UNIQUE,
  username TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  -- Timestamp ISO memorizzato come testo (SQLite).
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
