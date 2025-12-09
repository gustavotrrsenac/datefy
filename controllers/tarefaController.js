const db = require("../database");

module.exports = {
  async listar(req, res) {
    const { userId } = req.params;
    const [rows] = await db.query(
      "SELECT * FROM tarefas WHERE usuario_id = ? ORDER BY data DESC",
      [userId]
    );
    res.json(rows);
  },

  async recentes(req, res) {
    const { userId } = req.params;

    const [rows] = await db.query(
      "SELECT * FROM tarefas WHERE usuario_id = ? ORDER BY created_at DESC LIMIT 8",
      [userId]
    );

    res.json(rows);
  },

  async criar(req, res) {
    const { usuario_id, titulo, descricao, data, categoria } = req.body;

    await db.query(
      "INSERT INTO tarefas (usuario_id, titulo, descricao, data, categoria) VALUES (?, ?, ?, ?, ?)",
      [usuario_id, titulo, descricao, data, categoria]
    );

    res.json({ sucesso: true });
  },

  async editar(req, res) {
    const { id } = req.params;
    const { titulo, descricao, data, categoria, status } = req.body;

    await db.query(
      "UPDATE tarefas SET titulo=?, descricao=?, data=?, categoria=?, status=? WHERE id=?",
      [titulo, descricao, data, categoria, status, id]
    );

    res.json({ sucesso: true });
  },

  async remover(req, res) {
    const { id } = req.params;

    await db.query("DELETE FROM tarefas WHERE id=?", [id]);

    res.json({ sucesso: true });
  },
};
