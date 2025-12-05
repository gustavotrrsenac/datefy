const express = require("express");
const router = express.Router();
const tarefaController = require("../controllers/tarefaController");

router.get("/:userId", tarefaController.listar);
router.get("/recentes/:userId", tarefaController.recentes);
router.post("/", tarefaController.criar);
router.put("/:id", tarefaController.editar);
router.delete("/:id", tarefaController.remover);

module.exports = router;
