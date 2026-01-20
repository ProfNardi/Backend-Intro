Lingua: [Italiano](README.it.md) | [English](README.md)

# Backend Intro: Flask vs Express

Questa lezione mette a confronto due implementazioni simmetriche di un servizio backend. L'obiettivo e dimostrare che, nonostante le differenze di linguaggio tra i framework, i pattern logici (Routing, SSR, Auth, Database) rimangono costanti.

Useremo il Server-Side Rendering (SSR) per generare l'HTML direttamente sul server, una tecnica fondamentale per capire come i dati si trasformano in interfaccia.

- **[Express (Node.js)](https://expressjs.com/)**: E il pilastro degli stack moderni (MERN, PERN) e dei framework fullstack come Next.js o Astro. Usa il linguaggio JavaScript, onnipresente nel web. Come scelta di libreria di rendering, utilizzeremo **[EJS](https://ejs.co/)**, semplice e simile a HTML puro.

- **[Flask (Python)](https://flask.palletsprojects.com/en/stable/)**: E leggero, essenziale e perfetto per microservizi, prototipazione e progetti legati ai dati. Usa Python, noto per la sua sintassi chiara e la vasta libreria di pacchetti per applicazioni stand-alone. Come libreria di rendering, useremo **[Jinja2](https://pypi.org/project/Jinja2/)**, potente e flessibile.

- **[SQLite3](https://www.sqlite.org/)**: E il database relazionale leggero e file-based. Non richiede un server in esecuzione, usa SQL standard e permette a entrambi i backend (Flask e Express) di leggere e scrivere sulla stessa base dati in modo sicuro.

## Stack tecnologico
- **Python**: Flask + Jinja2 per il rendering.
- **Node.js**: Express + EJS per il rendering.
- **Database**: SQLite3 (file locale condiviso che memorizza la tabella `users`).
- **Autenticazione**: Sessioni server-side e hashing delle password con `bcrypt`.

## Roadmap delle route
- **GET /**: home pubblica con stato di login.
- **GET /login**: form di accesso.
- **POST /login**: autenticazione contro la tabella `users`.
- **GET /register**: form di registrazione.
- **POST /register**: creazione utente con password hashata.
- **GET /private**: area protetta (solo autenticati).
- **GET /logout**: terminazione sessione.
- **404 (fallback)**: pagina non trovata con link alla home.

## Diagramma di flusso (SSR)
1. L'utente invia `POST /register` o `POST /login`.
2. Il backend valida i dati e interroga SQLite3.
3. Il motore di template genera l'HTML con i dati necessari (username, errori, ecc.).
4. Il browser riceve la pagina gia pronta.

## Database: SQLite3
Centra tutta la logica su una tabella `users` controllata dall'applicazione e non da un backend esterno. Lo schema completo si trova in `database/schema.sql` e viene caricato automaticamente all'avvio.

```sql
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL UNIQUE,
  username TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

Ogni password viene memorizzata come hash `bcrypt`; nessun hash deve essere calcolato manualmente prima di salvare, la libreria si occupa di generare e verificare i digest corretti.

## Sicurezza: variabili d'ambiente
Copri gli ambienti con `database/.env` (uno solo, condiviso). Il file esistente include gia chiavi placeholder:

```
SQLITE_PATH="DATABASE.sqlite3"
SECRET_KEY="session_key_change_me123"
```

Le app usano `python-dotenv` e `dotenv` (Node) per caricare queste variabili. Qui `.env` resta nel repo a scopo didattico.

## Struttura cartelle

```
/{repo-root}
|-- database/
|   |-- .env
|   |-- db.py
|   |-- db.js
|   `-- schema.sql
|-- flask/
|   |-- requirements.txt
|   `-- templates/ (contiene home.html, login.html, register.html, 404.html)
|-- node/
|   |-- index.js
|   |-- package.json
|   `-- views/ (contiene home.ejs, login.ejs, register.ejs, 404.ejs)
|-- .gitignore (deve includere node_modules e il file .sqlite3)
|-- README.it.md
`-- README.md
```
Entrambi i progetti sono indipendenti e si collegano allo stesso database SQLite3.

## Setup rapido
Nessun server da avviare: il file del database viene creato all'avvio se non esiste gia.

### Flask

```Bash
cd flask
py -m pip install -r requirements.txt
py app.py # Ascolta su porta 5000
```

### Express (node/)
```Bash
cd node
npm install
npm start # Ascolta su porta 3000
```

Entrambe le app ascoltano su porte diverse (`5000` per Flask, `3000` per Express) ma condividono la stessa tabella `users`.
