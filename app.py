from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt

import sqlite3, os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "minha_chave_segura")
bcrypt = Bcrypt(app)

# --- BANCO DE DADOS ---
def get_db():
    conn = sqlite3.connect("usuarios.db")
    conn.row_factory = sqlite3.Row
    return conn

with get_db() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL
        )
    """)

# --- ROTAS ---
@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["password"]

        conn = get_db()
        user = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()

        if user and bcrypt.check_password_hash(user["senha_hash"], senha):
            session["user_id"] = user["id"]
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("E-mail ou senha incorretos.", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/criar-conta", methods=["GET", "POST"])
def criar_conta():
    if request.method == "POST":
        nome = request.form["full-name"]
        email = request.form["email"]
        senha = request.form["password"]
        confirmar = request.form["confirm-password"]

        if senha != confirmar:
            flash("As senhas não coincidem.", "danger")
            return redirect(url_for("criar_conta"))

        senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")

        try:
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
                    (nome, email, senha_hash),
                )
            flash("Conta criada com sucesso!", "success")
            return redirect(url_for("dashboard"))
        except sqlite3.IntegrityError:
            flash("E-mail já registrado.", "warning")
            return redirect(url_for("criar_conta"))

    return render_template("criar_conta.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/perfil")
def perfil():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("perfil.html")

@app.route("/recuperar-senha", methods=["GET", "POST"])
def recuperar_senha():
    if request.method == "POST":
        email = request.form["email"]
        flash(f"Se {email} estiver cadastrado, enviaremos instruções.", "info")
        return redirect(url_for("login"))
    return render_template("recuperar_senha.html")

@app.route("/resetar-senha")
def resetar_senha():
    return render_template("resetar_senha.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da conta.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run('0.0.0.0', 80, debug=True)
