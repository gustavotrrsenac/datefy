const db = require("../database");

module.exports = {
  async listar(req, res) {
    const { userId } = req.params;

    const [rows] = await db.query(
      "SELECT * FROM lembretes WHERE usuario_id = ? ORDER BY data ASC",
      [userId]
    );

    res.json(rows);
  },

  async criar(req, res) {
    const { usuario_id, tipo, descricao, data } = req.body;

    await db.query(
      "INSERT INTO lembretes (usuario_id, tipo, descricao, data) VALUES (?, ?, ?, ?)",
      [usuario_id, tipo, descricao, data]
    );

    res.json({ sucesso: true });
  },

  async remover(req, res) {
    const { id } = req.params;

    await db.query("DELETE FROM lembretes WHERE id=?", [id]);

    res.json({ sucesso: true });
  },
};
