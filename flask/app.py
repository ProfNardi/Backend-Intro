import importlib.util
import os
from pathlib import Path

from flask import Flask, redirect, render_template, request, session

DB_MODULE_PATH = Path(__file__).resolve().parents[1] / "database" / "db.py"
spec = importlib.util.spec_from_file_location("database.db", DB_MODULE_PATH)
db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db)

authenticate_user = db.authenticate_user
create_user = db.create_user

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev")  # Session cookie signing key.


@app.get("/")
def home():
    return render_template("public/home.html")


@app.get("/login")
def login_form():
    return render_template("public/login.html", error="")


@app.post("/login")
def login_post():
    email = (request.form.get("email") or "").strip()
    password = request.form.get("password") or ""

    if not email or not password:
        return render_template("public/login.html", error="Inserisci email e password")

    if not authenticate_user(email, password):
        return render_template("public/login.html", error="Credenziali non valide")

    session["user_email"] = email
    return redirect("/private")


@app.get("/register")
def register_form():
    return render_template("public/register.html", error="")


@app.post("/register")
def register_post():
    email = (request.form.get("email") or "").strip()
    password = request.form.get("password") or ""
    confirm = request.form.get("password_confirm") or ""

    if not email or not password or not confirm:
        return render_template("public/register.html", error="Completa tutti i campi")

    if password != confirm:
        return render_template("public/register.html", error="Le password non coincidono")

    if not create_user(email.split("@")[0], email, password):
        return render_template("public/register.html", error="Email già registrata")

    session["user_email"] = email
    return redirect("/private")


@app.get("/private")
def private_page():
    # Simple auth gate for the private page.
    email = session.get("user_email")
    if not email:
        return redirect("/login")
    return render_template("private/private.html", username=email.split("@")[0])


@app.get("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("public/404.html"), 404


if __name__ == "__main__":
    app.run()
