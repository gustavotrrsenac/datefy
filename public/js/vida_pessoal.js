// ======================================================
//  VIDA PESSOAL – SCRIPT DO FRONT
// ======================================================

// ELEMENTOS
const listaPessoal = document.getElementById("lista-pessoal");
const formPessoal = document.getElementById("form-pessoal");
const tituloInput = document.getElementById("titulo");
const dataInput = document.getElementById("data");
const descricaoInput = document.getElementById("descricao");
const btnSalvar = document.getElementById("btn-salvar");

let idEdit = null;

// ======================================================
//  1. CARREGAR DADOS DA VIDA PESSOAL
// ======================================================
async function carregarLembretes() {
    try {
        const response = await fetch("/api/vida-pessoal");
        const data = await response.json();

        listaPessoal.innerHTML = "";

        data.forEach(item => {
            listaPessoal.innerHTML += `
                <div class="card-pessoal">
                    <h3>${item.titulo}</h3>
                    <p>${item.descricao || ""}</p>
                    <span class="data">${item.data}</span>

                    <div class="acoes">
                        <button onclick="editarLembrete(${item.id})">Editar</button>
                        <button onclick="excluirLembrete(${item.id})" class="danger">Excluir</button>
                    </div>
                </div>
            `;
        });

    } catch (err) {
        console.error("Erro ao carregar vida pessoal:", err);
    }
}

carregarLembretes();

// ======================================================
//  2. SALVAR / EDITAR LEMBRETE
// ======================================================
formPessoal.addEventListener("submit", async (e) => {
    e.preventDefault();

    const dados = {
        titulo: tituloInput.value,
        data: dataInput.value,
        descricao: descricaoInput.value
    };

    try {
        let url = "/api/vida-pessoal";
        let method = "POST";

        if (idEdit) {
            url = `/api/vida-pessoal/${idEdit}`;
            method = "PUT";
        }

        await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        });

        formPessoal.reset();
        idEdit = null;
        btnSalvar.innerText = "Salvar Lembrete";

        carregarLembretes();

    } catch (err) {
        console.error("Erro ao salvar lembrete:", err);
    }
});

// ======================================================
//  3. EXCLUIR LEMBRETE
// ======================================================
async function excluirLembrete(id) {
    if (!confirm("Tem certeza que deseja excluir?")) return;

    await fetch(`/api/vida-pessoal/${id}`, { method: "DELETE" });

    carregarLembretes();
}

// ======================================================
//  4. EDITAR LEMBRETE
// ======================================================
async function editarLembrete(id) {
    try {
        const response = await fetch(`/api/vida-pessoal/${id}`);
        const item = await response.json();

        tituloInput.value = item.titulo;
        descricaoInput.value = item.descricao;
        dataInput.value = item.data;
        idEdit = id;

        btnSalvar.innerText = "Salvar Alterações";

    } catch (err) {
        console.error("Erro ao carregar item para edição:", err);
    }
}

// ======================================================
//  5. ATUALIZAR SALDO PESSOAL (caso exista)
// ======================================================
async function atualizarSaldo(valor) {
    try {
        await fetch("/api/vida-pessoal/saldo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ valor })
        });

    } catch (err) {
        console.error("Erro ao atualizar saldo:", err);
    }
}
