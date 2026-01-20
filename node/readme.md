# Express: endpoint pubblico + login con SQLite3

```bash
cd node
npm install
npm start
```

Configura `SQLITE_PATH` in `database/.env` se vuoi cambiare il nome del file DB. Lo schema viene caricato automaticamente da `database/schema.sql` all'avvio. Le password vengono hashate via `bcrypt`, quindi non calcolare manualmente l'hash prima di inviare i dati al server.

Visita `/login`, `/register` e `/private` per testare il flusso di autenticazione completo.
