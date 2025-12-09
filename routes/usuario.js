const express = require("express");
const router = express.Router();
const usuarioController = require("../controllers/usuarioController");

router.get("/:id", usuarioController.buscar);
router.put("/:id", usuarioController.atualizar);

module.exports = router;
