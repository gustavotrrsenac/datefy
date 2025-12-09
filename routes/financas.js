const express = require("express");
const router = express.Router();
const financaController = require("../controllers/financaController");

router.get("/:userId", financaController.listar);
router.get("/totais/:userId", financaController.totais);
router.post("/", financaController.criar);
router.delete("/:id", financaController.remover);

module.exports = router;
