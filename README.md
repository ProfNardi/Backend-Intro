Language: [English](README.md) | [Italiano](README.it.md)

# Backend Intro: Flask vs Express

This lesson compares two symmetric backend implementations. The goal is to show that, despite language differences, the logical patterns (routing, SSR, auth, database) stay the same.

We use Server-Side Rendering (SSR) to generate HTML directly on the server, a key technique to understand how data becomes interface.

- **[Express (Node.js)](https://expressjs.com/)**: A pillar of modern stacks (MERN, PERN) and fullstack frameworks like Next.js or Astro. It uses JavaScript, the web's lingua franca. For rendering, we use **[EJS](https://ejs.co/)**, simple and close to plain HTML.

- **[Flask (Python)](https://flask.palletsprojects.com/en/stable/)**: Lightweight and essential, perfect for microservices, prototyping, and data-driven projects. It uses Python, known for its clear syntax and rich ecosystem. For rendering, we use **[Jinja2](https://pypi.org/project/Jinja2/)**, powerful and flexible.

- **[SQLite3](https://www.sqlite.org/)**: A lightweight, file-based relational database. It does not require a running server, uses standard SQL, and allows both backends (Flask and Express) to read and write the same data safely.

## Tech stack
- **Python**: Flask + Jinja2 for rendering.
- **Node.js**: Express + EJS for rendering.
- **Database**: SQLite3 (local file that stores the `users` table).
- **Authentication**: Server-side sessions and password hashing with `bcrypt`.

## Route roadmap
- **GET /**: public home with login status.
- **GET /login**: login form.
- **POST /login**: auth against the `users` table.
- **GET /register**: registration form.
- **POST /register**: user creation with hashed password.
- **GET /private**: protected area (authenticated only).
- **GET /logout**: end session.
- **404 (fallback)**: not found page with link to home.

## Flow (SSR)
1. The user submits `POST /register` or `POST /login`.
2. The backend validates data and queries SQLite3.
3. The template engine renders HTML with needed data (username, errors, etc.).
4. The browser receives a ready-to-display page.

## Database: SQLite3
All logic is centered on a `users` table controlled by the application, not by an external backend. The full schema is in `database/schema.sql` and is loaded automatically at startup.

```sql
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL UNIQUE,
  username TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

Each password is stored as a `bcrypt` hash; no hash should be computed manually before saving, the library handles correct hashing and verification.

## Security: environment variables
Use `database/.env` (a single shared file). The existing file includes placeholder keys:

```
SQLITE_PATH="DATABASE.sqlite3"
SECRET_KEY="session_key_change_me123"
```

The apps use `python-dotenv` and `dotenv` (Node) to load these variables. Here `.env` stays in the repo for teaching purposes.

## Folder structure

```
/{repo-root}
|-- database/
|   |-- .env
|   |-- db.py
|   |-- db.js
|   `-- schema.sql
|-- flask/
|   |-- requirements.txt
|   `-- templates/ (contains home.html, login.html, register.html, 404.html)
|-- node/
|   |-- index.js
|   |-- package.json
|   `-- views/ (contains home.ejs, login.ejs, register.ejs, 404.ejs)
|-- .gitignore (should include node_modules and the .sqlite3 file)
|-- README.it.md
`-- README.md
```
Both projects are independent and connect to the same SQLite3 database.

## Quick setup
No server to start: the database file is created at startup if it does not exist.

### Flask

```Bash
cd flask
py -m pip install -r requirements.txt
py app.py # Listens on port 5000
```

### Express (node/)
```Bash
cd node
npm install
npm start # Listens on port 3000
```

Both apps listen on different ports (`5000` for Flask, `3000` for Express) but share the same `users` table.
