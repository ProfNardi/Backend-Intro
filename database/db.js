const fs = require("fs");
const path = require("path");
const { createRequire } = require("module");

// --- CONFIGURAZIONE DIPENDENZE ---
const requireFromNode = createRequire(path.join(__dirname, "..", "node", "index.js"));
const bcrypt = requireFromNode("bcrypt");
const Database = requireFromNode("better-sqlite3");

requireFromNode("dotenv").config({ 
    path: path.join(__dirname, ".env") 
});

// --- CONFIGURAZIONE DATABASE ---
const rawDbPath = process.env.SQLITE_PATH || "DATABASE.sqlite3";
const dbPath = path.isAbsolute(rawDbPath) 
    ? rawDbPath 
    : path.join(__dirname, rawDbPath);

const db = new Database(dbPath);

// Inizializzazione Database
db.pragma("busy_timeout = 5000");
const schema = fs.readFileSync(path.join(__dirname, "schema.sql"), "utf8");
db.exec(schema);

// --- LOGICA UTENTI ---

/**
 * Registra un nuovo utente nel database
 */
async function createUser(username, email, password) {
    const saltRounds = 12;
    const passwordHash = await bcrypt.hash(password, saltRounds);

    try {
        const stmt = db.prepare(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)"
        );
        stmt.run(username, email, passwordHash);
        return true;
    } catch (error) {
        // Gestione errore duplicati (email/username già esistenti)
        if (error?.code?.startsWith("SQLITE_CONSTRAINT")) {
            return false;
        }
        throw error;
    }
}

/**
 * Verifica le credenziali di un utente
 */
async function authenticateUser(email, password) {
    const query = "SELECT password_hash FROM users WHERE email = ?";
    const row = db.prepare(query).get(email);

    if (!row) return false;

    return await bcrypt.compare(password, row.password_hash);
}

// --- ESPORTAZIONE ---
module.exports = { 
    createUser, 
    authenticateUser 
};