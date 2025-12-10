const express = require("express");
const router = express.Router();
const lembreteController = require("../controllers/lembreteController");

router.get("/:userId", lembreteController.listar);
router.post("/", lembreteController.criar);
router.delete("/:id", lembreteController.remover);

module.exports = router;
