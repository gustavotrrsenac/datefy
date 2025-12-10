from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_bcrypt import Bcrypt
import os
# --- PEEWEE / MYSQL IMPORTS ---
from peewee import *
from playhouse.shortcuts import model_to_dict
from decimal import Decimal
from datetime import datetime

# ------------------------------

app = Flask(__name__)
# A chave secreta é usada para sessões.
app.secret_key = os.getenv("SECRET_KEY", "minha_chave_segura")
bcrypt = Bcrypt(app)

# ---------------- CONFIGURAÇÕES DO MYSQL COM PEEWEE ----------------
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "senac")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "datefy_db")

# Configuração do banco de dados Peewee (MySQL)
db = MySQLDatabase(
    MYSQL_DATABASE,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
)

# --- Definição dos Modelos (Mapeamento ORM) ---
class BaseModel(Model):
    class Meta:
        database = db

class Usuario(BaseModel):
    nome = CharField()
    email = CharField(unique=True)
    senha_hash = CharField()

    class Meta:
        table_name = 'usuarios'

class Tarefa(BaseModel):
    user = ForeignKeyField(Usuario, backref='tarefas', column_name='user_id')
    titulo = CharField()
    descricao = TextField(null=True)
    data = CharField()  # Formato YYYY-MM-DD
    categoria = CharField(null=True)
    status = IntegerField(default=0)  # 0: pendente, 1: concluída

    class Meta:
        table_name = 'tarefas'

class Financa(BaseModel):
    usuario = ForeignKeyField(Usuario, backref='financas', column_name='usuario_id')
    descricao = CharField(null=True)
    categoria = CharField(null=True)
    tipo = CharField(max_length=10)  # 'entrada' ou 'saida'
    valor = FloatField()
    forma_pagamento = CharField(null=True)
    parcelas = IntegerField(default=1)
    data = CharField(null=True)  # YYYY-MM-DD

    class Meta:
        table_name = 'financas'

# --- Hooks para gerenciamento de conexão (Peewee/Flask) ---
@app.before_request
def before_request():
    """Abre a conexão antes de processar a requisição (se necessário)."""
    try:
        if db.is_closed():
            db.connect()
    except Exception as e:
        # evita quebrar a aplicação inteira caso o DB esteja indisponível
        app.logger.exception("Falha ao conectar ao banco: %s", e)

@app.teardown_request
def teardown_request(exception):
    """Garante o fechamento da conexão mesmo em exceções."""
    try:
        if not db.is_closed():
            db.close()
    except Exception:
        pass

# --- Criação das tabelas necessárias (apenas durante desenvolvimento) ---
def create_tables():
    with db:
        db.create_tables([Usuario, Tarefa, Financa], safe=True)

try:
    create_tables()
except Exception as e:
    app.logger.warning("Não foi possível criar tabelas automaticamente: %s", e)

# --- Categorias ---
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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("password", "").strip()

        try:
            user_model = Usuario.get(Usuario.email == email)
        except DoesNotExist:
            user_model = None

        if user_model and bcrypt.check_password_hash(user_model.senha_hash, senha):
            session["user_id"] = user_model.id
            session["nome"] = user_model.nome
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("dashboard"))

        flash("E-mail ou senha incorretos.", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/criar-conta", methods=["GET", "POST"])
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
            Usuario.create(
                nome=nome,
                email=email,
                senha_hash=senha_hash
            )
            flash("Conta criada com sucesso! Faça login.", "success")
            return redirect(url_for("login"))
        except IntegrityError:
            flash("E-mail já registrado.", "warning")
            return redirect(url_for("criar_conta"))
        except Exception as e:
            app.logger.exception("Erro ao criar conta: %s", e)
            flash("Erro ao criar conta.", "danger")
            return redirect(url_for("criar_conta"))

    return render_template("criar_conta.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da conta.", "info")
    return redirect(url_for("login"))

# ---------------- API PARA TAREFAS (CALENDÁRIO) ----------------
@app.route("/api/tarefas")
def api_tarefas():
    if "user_id" not in session:
        return jsonify({"error": "Não autorizado"}), 401

    user_id = session["user_id"]

    tarefas = (Tarefa
               .select(Tarefa.titulo, Tarefa.data)
               .where((Tarefa.user == user_id) & (Tarefa.status == 0))
               .dicts()
              )

    eventos = []
    for tarefa in tarefas:
        # Garante que a data esteja no formato ISO (YYYY-MM-DD)
        eventos.append({
            "title": tarefa["titulo"],
            "start": tarefa["data"],
            "allDay": True,
            "color": "#FF5722"
        })

    return jsonify(eventos)

# ---------------- ROTAS PRINCIPAIS ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # Soma das saídas
    saidas = (Financa
               .select(fn.SUM(Financa.valor))
               .where((Financa.usuario == user_id) & (Financa.tipo == 'saida'))
               .scalar())

    # Soma das entradas
    entradas = (Financa
               .select(fn.SUM(Financa.valor))
               .where((Financa.usuario == user_id) & (Financa.tipo == 'entrada'))
               .scalar())

    # Normaliza None para 0
    entradas = float(entradas) if entradas is not None else 0.0
    saidas = float(saidas) if saidas is not None else 0.0

    totalGastos = entradas - saidas

    # tarefasDoDia: exemplo simples contando tarefas pendentes com a data de hoje
    hoje = datetime.now().date().isoformat()
    tarefasDoDia = (Tarefa
                    .select()
                    .where((Tarefa.user == user_id) & (Tarefa.data == hoje) & (Tarefa.status == 0))
                    .count())

    return render_template(
        "dashboard.html",
        nome=session.get("nome", "Usuário"),
        tg=totalGastos,
        td=tarefasDoDia,
        entradas=entradas,
        saidas=saidas
    )

@app.route("/perfil")
def perfil():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    try:
        user_model = Usuario.get_by_id(user_id)
        usuario = model_to_dict(user_model, only=[Usuario.nome, Usuario.email])
    except DoesNotExist:
        usuario = None

    return render_template("perfil.html", usuario=usuario)

# ---------------- VIDA PESSOAL / TAREFAS ----------------
@app.route("/vida-pessoal")
def vida_pessoal():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    tarefas = (Tarefa
               .select()
               .where(Tarefa.user == user_id)
               .order_by(Tarefa.data.asc())
               .dicts()
              )

    return render_template("vida_pessoal.html", tarefas=tarefas)

@app.route("/add-tarefa")
def add_tarefa():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("tarefas.html")

@app.route("/salvar-tarefa", methods=["POST"])
def salvar_tarefa():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()
    data = request.form.get("data", "").strip()
    categoria = request.form.get("categoria", "").strip()

    Tarefa.create(
        user=user_id,
        titulo=titulo,
        descricao=descricao,
        data=data,
        categoria=categoria
    )

    flash("Tarefa adicionada com sucesso!", "success")
    return redirect(url_for("vida_pessoal"))

@app.route("/concluir-tarefa/<int:id>")
def concluir_tarefa(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    query = Tarefa.update(status=1).where((Tarefa.id == id) & (Tarefa.user == user_id))
    query.execute()

    flash("Tarefa concluída!", "success")
    return redirect(url_for("vida_pessoal"))

@app.route("/desfazer-tarefa/<int:id>")
def desfazer_tarefa(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    query = Tarefa.update(status=0).where((Tarefa.id == id) & (Tarefa.user == user_id))
    query.execute()

    flash("Tarefa marcada como pendente.", "warning")
    return redirect(url_for("vida_pessoal"))

# ---------------- FINANÇAS ----------------
@app.route("/financas", methods=["GET", "POST"]) 
def financas():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

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

        Financa.create(
            usuario=user_id,
            descricao=descricao,
            categoria=categoria,
            tipo=tipo,
            valor=valor,
            forma_pagamento=forma,
            parcelas=parcelas,
            data=data
        )

        flash("Registro financeiro salvo.", "success")
        return redirect(url_for("financas"))

    registros = (Financa
                 .select()
                 .where(Financa.usuario == user_id)
                 .order_by(Financa.data.desc())
                 .dicts()
                )

    return render_template("financas.html", registros=registros, categorias=CATEGORIAS)

@app.route("/financas/data")
def financas_data():
    if "user_id" not in session:
        return jsonify({"error": "unauthorized"}), 401

    user_id = session["user_id"]

    # 1. Totais de Entrada e Saída
    totals = (Financa
              .select(Financa.tipo, fn.SUM(Financa.valor).alias('total'))
              .where(Financa.usuario == user_id)
              .group_by(Financa.tipo)
              .dicts()
             )

    tot_dict = {"entrada": 0.0, "saida": 0.0}
    for row in totals:
        tot_dict[row["tipo"]] = float(row["total"]) if row["total"] is not None else 0.0

    # 2. Totais por Categoria
    cat_rows = (Financa
                .select(Financa.categoria, Financa.tipo, fn.SUM(Financa.valor).alias('total'))
                .where(Financa.usuario == user_id)
                .group_by(Financa.categoria, Financa.tipo)
                .dicts()
               )

    cat_map = {}
    for c in CATEGORIAS:
        cat_map[c["key"]] = {"label": c["label"], "color": c["color"], "total": 0.0}

    for r in cat_rows:
        key = r["categoria"] or "outras"
        if key not in cat_map:
            cat_map[key] = {"label": key, "color": "#999999", "total": 0.0}

        valor_total = float(r["total"]) if r["total"] is not None else 0.0

        if r["tipo"] == "entrada":
            cat_map[key]["total"] += valor_total
        else:
            cat_map[key]["total"] -= valor_total

    labels, values, colors = [], [], []
    for k, v in cat_map.items():
        if abs(v["total"]) > 0:
            labels.append(v["label"])
            values.append(round(v["total"], 2))
            colors.append(v["color"])

    return jsonify({"totais": tot_dict, "por_categoria": {"labels": labels, "values": values, "colors": colors}})

@app.route("/recuperar-senha", methods=["GET", "POST"])
def recuperar_senha():
    if request.method == "POST":
        email = request.form.get("email")
        flash(f"Se {email} estiver cadastrado, enviaremos instruções por e-mail (simulado).", "info")
        return redirect(url_for("login"))
    return render_template("recuperar_senha.html")

@app.route("/editar_perfil", methods=["GET", "POST"])
def editar_perfil():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]

        query = Usuario.update(nome=nome, email=email).where(Usuario.id == user_id)
        query.execute()

        session["nome"] = nome
        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for("perfil"))

    try:
        user_model = Usuario.get_by_id(user_id)
        usuario = model_to_dict(user_model, only=[Usuario.nome, Usuario.email])
    except DoesNotExist:
        usuario = None

    return render_template("editar_perfil.html", usuario=usuario)

# ----------------- APAGAR FINANCA -----------------
@app.route("/apagar/<int:id>", methods=["POST"])
def apagar_registro(id):
    try:
        # Tenta apagar o registro pelo ID
        query = Financa.delete().where(Financa.id == id)
        query.execute()

        flash("Registro apagado com sucesso!", "success")

    except Exception as e:
        flash(f"Erro ao apagar o registro: {e}", "danger")

    return redirect(url_for("financas"))


# ----------------- APAGAR TAREFAS -----------------

@app.route("/excluir_tarefa/<int:id>")
def excluir_tarefa(id):
    try:
        Tarefa.delete().where(Tarefa.id == id).execute()
        flash("Tarefa excluída com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao excluir a tarefa: {e}", "danger")

    return redirect(url_for("vida_pessoal"))

# ---------------- TESTE NOTICAÇÕES ----------------
@app.route("/salvar_preferencias", methods=["POST"])
def salvar_preferencias():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    user = Usuario.get_or_none(Usuario.id == user_id)

    if not user:
        flash("Usuário não encontrado.", "error")
        return redirect(url_for("perfil"))

    # DADOS PESSOAIS
    user.nome = request.form.get("nome")
    user.email = request.form.get("email")

    # NOTIFICAÇÕES
    user.notif_email = "email_alertas" in request.form
    user.notif_push = "push_alertas" in request.form
    user.notif_relatorio = "mensal_relatorio" in request.form

    # SENHAS
    senha_atual = request.form.get("senha_atual")
    nova_senha = request.form.get("nova_senha")
    confirmar = request.form.get("confirmar_senha")

    # Alterar senha se os campos estiverem preenchidos corretamente 
    if senha_atual and nova_senha and nova_senha == confirmar:
        if check_password(user.senha, senha_atual):
            user.senha = generate_password(nova_senha)

    user.save()

    flash("Preferências e perfil atualizados!", "success")
    return redirect(url_for("perfil"))

# Correção final da execução Flask com 'port' como inteiro
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
