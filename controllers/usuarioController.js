const db = require("../database");

module.exports = {
  async buscar(req, res) {
    const { id } = req.params;

    const [rows] = await db.query("SELECT * FROM usuarios WHERE id=?", [id]);

    res.json(rows[0]);
  },

  async atualizar(req, res) {
    const { id } = req.params;
    const { nome, email, balance } = req.body;

    await db.query(
      "UPDATE usuarios SET nome=?, email=?, balance=? WHERE id=?",
      [nome, email, balance, id]
    );

    res.json({ sucesso: true });
  },
};
