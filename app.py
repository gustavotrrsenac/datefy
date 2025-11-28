from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_bcrypt import Bcrypt
import sqlite3, os
from decimal import Decimal

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "minha_chave_segura")
bcrypt = Bcrypt(app)

DB_PATH = "usuarios.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- criar tabelas necessárias (usuarios, tarefas, financas) ---
with get_db() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT,
            data TEXT NOT NULL,
            categoria TEXT,
            status INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES usuarios(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS financas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            descricao TEXT,
            categoria TEXT,
            tipo TEXT,
            valor REAL,
            forma_pagamento TEXT,
            parcelas INTEGER,
            data TEXT,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    """)
    conn.commit()

# --- categorias (opção 2) ---
CATEGORIAS = [
    {"key": "salario", "label": "Salário/Trabalho", "color": "#4CAF50"},
    {"key": "casa", "label": "Casa", "color": "#2196F3"},
    {"key": "utilidades", "label": "Utilidades", "color": "#FF9800"},
    {"key": "alimentacao", "label": "Alimentação", "color": "#FF5722"},
    {"key": "transporte", "label": "Transporte", "color": "#9C27B0"},
    {"key": "parcelas", "label": "Créditos / Parcelas", "color": "#795548"},
    {"key": "mercado", "label": "Mercado", "color": "#3F51B5"},
    {"key": "saude", "label": "Saúde", "color": "#E91E63"},
    {"key": "tecnologia", "label": "Tecnologia", "color": "#00BCD4"},
    {"key": "lazer", "label": "Lazer", "color": "#FFC107"},
]

# ---------------- ROTAS AUTENTICAÇÃO ----------------
@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("password", "").strip()
        conn = get_db()
        user = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
        conn.close()
        if user and bcrypt.check_password_hash(user["senha_hash"], senha):
            session["user_id"] = user["id"]
            session["nome"] = user["nome"]
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("dashboard"))
        flash("E-mail ou senha incorretos.", "danger")
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/criar-conta", methods=["GET","POST"])
def criar_conta():
    if request.method == "POST":
        nome = request.form.get("full-name", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("password", "")
        confirmar = request.form.get("confirm-password", "")
        if senha != confirmar:
            flash("As senhas não coincidem.", "danger")
            return redirect(url_for("criar_conta"))
        senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")
        try:
            with get_db() as conn:
                conn.execute("INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
                             (nome, email, senha_hash))
            flash("Conta criada com sucesso! Faça login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("E-mail já registrado.", "warning")
            return redirect(url_for("criar_conta"))
    return render_template("criar_conta.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da conta.", "info")
    return redirect(url_for("login"))

# ---------------- ROTAS PRINCIPAIS ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    # tarefas do dia (hoje) e resumo financeiro são carregados via JS/rotas
    return render_template("dashboard.html", nome=session.get("nome","Usuário"))

@app.route("/perfil")
def perfil():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    user = conn.execute("SELECT nome, email FROM usuarios WHERE id = ?", (session["user_id"],)).fetchone()

    return render_template("perfil.html", nome=user["nome"], email=user["email"])


# ---------------- VIDA PESSOAL / TAREFAS ----------------
@app.route("/vida-pessoal")
def vida_pessoal():
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    tarefas = conn.execute("SELECT * FROM tarefas WHERE user_id = ? ORDER BY data ASC", (session["user_id"],)).fetchall()
    conn.close()
    return render_template("vida_pessoal.html", tarefas=tarefas)

@app.route("/add-tarefa")
def add_tarefa():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("tarefas.html")  # usamos tarefas.html como formulário de adicionar

@app.route("/salvar-tarefa", methods=["POST"])
def salvar_tarefa():
    if "user_id" not in session:
        return redirect(url_for("login"))
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()
    data = request.form.get("data", "").strip()
    categoria = request.form.get("categoria", "").strip()
    with get_db() as conn:
        conn.execute("INSERT INTO tarefas (user_id, titulo, descricao, data, categoria) VALUES (?, ?, ?, ?, ?)",
                     (session["user_id"], titulo, descricao, data, categoria))
    flash("Tarefa adicionada com sucesso!", "success")
    return redirect(url_for("vida_pessoal"))

@app.route("/concluir-tarefa/<int:id>")
def concluir_tarefa(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    with get_db() as conn:
        conn.execute("UPDATE tarefas SET status = 1 WHERE id = ? AND user_id = ?", (id, session["user_id"]))
    flash("Tarefa concluída!", "success")
    return redirect(url_for("vida_pessoal"))

@app.route("/desfazer-tarefa/<int:id>")
def desfazer_tarefa(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    with get_db() as conn:
        conn.execute("UPDATE tarefas SET status = 0 WHERE id = ? AND user_id = ?", (id, session["user_id"]))
    flash("Tarefa marcada como pendente.", "warning")
    return redirect(url_for("vida_pessoal"))

# ---------------- FINANÇAS ----------------
@app.route("/financas", methods=["GET","POST"])
def financas():
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    if request.method == "POST":
        descricao = request.form.get("descricao", "").strip()
        categoria = request.form.get("categoria")
        tipo = request.form.get("tipo")
        valor_raw = request.form.get("valor", "0").replace(",", ".").strip()
        forma = request.form.get("forma_pagamento", "")
        parcelas = request.form.get("parcelas") or 1
        data = request.form.get("data") or ""
        try:
            valor = float(Decimal(valor_raw))
            parcelas = int(parcelas)
        except Exception:
            flash("Valor ou parcelas inválidos.", "danger")
            return redirect(url_for("financas"))
        conn.execute("""INSERT INTO financas (usuario_id, descricao, categoria, tipo, valor, forma_pagamento, parcelas, data)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                     (session["user_id"], descricao, categoria, tipo, valor, forma, parcelas, data))
        conn.commit()
        flash("Registro financeiro salvo.", "success")
        conn.close()
        return redirect(url_for("financas"))
    rows = conn.execute("SELECT * FROM financas WHERE usuario_id=? ORDER BY data DESC", (session["user_id"],)).fetchall()
    conn.close()
    return render_template("financas.html", registros=rows, categorias=CATEGORIAS)

@app.route("/financas/data")
def financas_data():
    if "user_id" not in session:
        return jsonify({"error":"unauthorized"}), 401
    conn = get_db()
    user_id = session["user_id"]
    totals = conn.execute("SELECT tipo, COALESCE(SUM(valor),0) as total FROM financas WHERE usuario_id = ? GROUP BY tipo", (user_id,)).fetchall()
    tot_dict = {"entrada":0.0, "saida":0.0}
    for row in totals:
        tot_dict[row["tipo"]] = float(row["total"])
    cat_rows = conn.execute("SELECT categoria, tipo, COALESCE(SUM(valor),0) as total FROM financas WHERE usuario_id = ? GROUP BY categoria, tipo", (user_id,)).fetchall()
    cat_map = {}
    for c in CATEGORIAS:
        cat_map[c["key"]] = {"label": c["label"], "color": c["color"], "total": 0.0}
    for r in cat_rows:
        key = r["categoria"]
        if key not in cat_map:
            cat_map[key] = {"label": key, "color":"#999999", "total":0.0}
        if r["tipo"] == "entrada":
            cat_map[key]["total"] += float(r["total"])
        else:
            cat_map[key]["total"] -= float(r["total"])
    labels, values, colors = [], [], []
    for k,v in cat_map.items():
        if abs(v["total"]) > 0:
            labels.append(v["label"])
            values.append(round(v["total"],2))
            colors.append(v["color"])
    conn.close()
    return jsonify({"totais": tot_dict, "por_categoria": {"labels": labels, "values": values, "colors": colors}})

# --- recuperar senha (simulado) ---
@app.route("/recuperar-senha", methods=["GET","POST"])
def recuperar_senha():
    if request.method == "POST":
        email = request.form.get("email")
        flash(f"Se {email} estiver cadastrado, enviaremos instruções por e-mail (simulado).", "info")
        return redirect(url_for("login"))
    return render_template("recuperar_senha.html")

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/perfil')
def perfil():
    # Exemplo: dados fictícios do usuário
    usuario = {
        "nome": "Barbara",
        "email": "barbara@email.com",
        "data_cadastro": "20/11/2025"
    }
    return render_template('perfil.html', usuario=usuario)

@app.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil():
    if request.method == 'POST':
        # Aqui você trataria os dados enviados pelo formulário
        nome = request.form['nome']
        email = request.form['email']
        # salvar no banco...
        return redirect(url_for('perfil'))
    return render_template('editar_perfil.html')

@app.route('/perfil')
def perfil():
    user = {"nome": "Barbara", "email": "barbara@email.com"}
    return render_template("perfil.html", nome=user["nome"], email=user["email"])
