const db = require("../database");
const bcrypt = require("bcrypt");

module.exports = {
  async registrar(req, res) {
    const { nome, email, senha } = req.body;

    const hash = await bcrypt.hash(senha, 10);

    try {
      await db.query(
        "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
        [nome, email, hash]
      );
      res.json({ sucesso: true });
    } catch (err) {
      res.status(400).json({ erro: "Email já cadastrado." });
    }
  },

  async login(req, res) {
    const { email, senha } = req.body;

    const [rows] = await db.query("SELECT * FROM usuarios WHERE email = ?", [
      email,
    ]);

    if (rows.length === 0)
      return res.status(400).json({ erro: "Usuário não encontrado" });

    const usuario = rows[0];

    const ok = await bcrypt.compare(senha, usuario.senha);

    if (!ok) return res.status(400).json({ erro: "Senha incorreta" });

    res.json({
      sucesso: true,
      usuario: {
        id: usuario.id,
        nome: usuario.nome,
        email: usuario.email,
      },
    });
  },
};
