const db = require("../database");

module.exports = {
  async listar(req, res) {
    const { userId } = req.params;

    const [rows] = await db.query(
      "SELECT * FROM financas WHERE usuario_id = ? ORDER BY data DESC",
      [userId]
    );

    res.json(rows);
  },

  async totais(req, res) {
    const { userId } = req.params;

    const [rows] = await db.query(
      `SELECT 
        SUM(CASE WHEN tipo='entrada' THEN valor END) AS entrada,
        SUM(CASE WHEN tipo='saida' THEN valor END) AS saida
      FROM financas WHERE usuario_id = ?`,
      [userId]
    );

    res.json(rows[0]);
  },

  async criar(req, res) {
    const { usuario_id, tipo, valor, descricao, data } = req.body;

    await db.query(
      "INSERT INTO financas (usuario_id, tipo, valor, descricao, data) VALUES (?, ?, ?, ?, ?)",
      [usuario_id, tipo, valor, descricao, data]
    );

    res.json({ sucesso: true });
  },

  async remover(req, res) {
    const { id } = req.params;

    await db.query("DELETE FROM financas WHERE id=?", [id]);

    res.json({ sucesso: true });
  },
};
