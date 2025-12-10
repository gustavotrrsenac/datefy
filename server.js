const express = require("express");
const cors = require("cors");
const app = express();

app.use(express.json());
app.use(cors());
app.use(express.static("public"));

app.use("/auth", require("./routes/auth"));
app.use(express.static(__dirname + "/static"));
app.use("/tarefas", require("./routes/tarefas"));
app.use("/financas", require("./routes/financas"));
app.use("/lembretes", require("./routes/lembretes"));
app.use("/usuario", require("./routes/usuario"));
app.get("/", (req, res) => {
  res.sendFile(__dirname + "/templates/dashboard.html");
});

app.listen(3000, () => {
  console.log("Servidor rodando em http://localhost:3000");
});
