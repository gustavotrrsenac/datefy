# 🗓️ Datefy: Seu Calendário Financeiro e de Rotinas

## Sobre o Projeto

**Datefy** é um projeto de software com o objetivo de **gerenciar rotinas pessoais, financeiras e profissionais de forma intuitiva e simplificada** [1]. Atuando como um **Calendário Financeiro** [1], ele centraliza tarefas, contas e eventos em uma única plataforma visual e interativa.

O sistema foi concebido para oferecer uma visão clara e organizada das obrigações do usuário, integrando a gestão de tempo com o controle financeiro.

## Funcionalidades Principais (Requisitos Funcionais)

O Datefy oferece um conjunto robusto de funcionalidades para a gestão completa do dia a dia:

| Categoria | Funcionalidade | Descrição |
| :--- | :--- | :--- |
| **Autenticação e Perfil** | `RF01` Cadastro de Usuário | Permite o registro de nome, e-mail e senha. |
| | `RF02` Login | Acesso seguro mediante validação de credenciais. |
| | `RF03` Recuperar Senha | Permite a recuperação de senha via e-mail. |
| | `RF04` Edição de Perfil | Visualização e edição de informações do perfil (nome, foto, e-mail, senha). |
| | `RF18` Logout | Encerramento seguro da sessão. |
| **Gestão de Lembretes** | `RF05` Criação de Lembretes | Criação de lembretes com título, tipo (tarefa, conta ou evento), descrição, data/hora, prioridade, categoria, status e notificação. |
| | `RF06` Edição de Lembretes | Alteração de informações de lembretes existentes. |
| | `RF07` Exclusão de Lembretes | Permite apenas arquivamento ou conclusão, seguindo a regra de negócio que impede a exclusão definitiva. |
| | `RF08` Listagem de Lembretes | Visualização de lembretes ativos, pendentes e concluídos em lista ou calendário. |
| | `RF15` Compartilhamento | Permite compartilhar lembretes com outros usuários (visualização). |
| | `RF16` Anexar Arquivos | Possibilidade de anexar documentos, imagens ou comprovantes. |
| | `RF17` Filtro e Busca | Busca e filtragem por título, categoria, data, prioridade e status. |
| **Gestão Financeira** | `RF10` Registro de Gastos | Registro de despesas com valor, categoria, forma de pagamento e data. |
| | `RF11` Registro de Entradas | Registro de receitas (salário, ganhos extras) com valor, data e categoria. |
| | `RF12` Balanço Financeiro | Resumo financeiro com total de entradas, saídas e saldo, com opção de filtragem por período. |
| **Visualização e Notificação** | `RF09` Gerenciamento de Notificações | Configuração de horário, frequência e modo de alerta (som, vibração, pop-up). |
| | `RF13` Registro de Evento e Tarefas | Registro de itens não financeiros vinculados ao calendário. |
| | `RF14` Visualização do Calendário | Exibição visual e interativa de todos os itens, destacando prioridades e cores. |

## Regras de Negócio (Business Rules)

As seguintes regras de negócio guiam o comportamento do sistema [1]:

*   **R1:** Todo lembrete deve conter título, tipo, data/hora, prioridade, categoria e status.
*   **R2:** Lembretes não podem ser excluídos definitivamente — apenas concluídos ou arquivados.
*   **R3:** Proíbe duplicidade de lembretes com o mesmo título e data/hora.
*   **R4:** Cada lembrete é uma entidade independente (não há "projetos").
*   **R7:** A tela principal mostra apenas lembretes ativos e pendentes.
*   **R8:** A criação de um lembrete gera uma notificação automática.
*   **R9:** Lembretes podem ser compartilhados entre usuários.

## Qualidade e Segurança (Requisitos Não Funcionais)

O projeto Datefy adere a rigorosos padrões de qualidade, desempenho e segurança [1]:

| Categoria | Requisito | Descrição |
| :--- | :--- | :--- |
| **Desempenho** | `RNF01` Carregamento | Tela principal carrega em até 3 segundos. |
| | `RNF02` Resposta | Operações de CRUD de lembretes processadas em até 2 segundos. |
| | `RNF03` Escalabilidade | Suporte a até 100 usuários ativos simultaneamente. |
| **Segurança** | `RNF04` Criptografia | Senhas armazenadas com criptografia segura (ex: Bcrypt ou Argon2). |
| | `RNF05` Comunicação | Toda a comunicação via protocolo HTTPS. |
| | `RNF06` Autenticação | Uso de tokens (ex: JWT) e encerramento de sessão após 15 minutos de inatividade. |
| | `RNF15` Auditoria | Registro de logs de ações críticas (login, exclusão/edição de lembretes). |
| **Arquitetura** | `RNF10` Manutenibilidade | Código-fonte modular para facilitar atualizações. |
| | `RNF11` Versionamento | Uso de Git para controle de mudanças. |
| | `RNF13` APIs | APIs seguem o padrão RESTful. |
| **Disponibilidade** | `RNF14` Uptime | Disponibilidade de pelo menos 99% do tempo. |
| | `RNF08` Backup | Backup automático diário dos dados. |
| | `RNF09` Recuperação | Retorno ao último estado consistente em caso de falhas. |
| **Usabilidade** | `RNF07` Interface | Interface intuitiva, minimalista e responsiva (desktop e mobile). |
| | `RNF12` Compatibilidade | Compatível com os principais navegadores modernos. |

## Tecnologias (A Definir)

Embora o PDF não especifique as tecnologias exatas, a menção a **RESTful APIs** (`RNF13`), **criptografia de senhas** (`RNF04`), **tokens JWT** (`RNF06`) e **Git** (`RNF11`) sugere uma arquitetura moderna de aplicação web, provavelmente utilizando:

*   **Frontend:** Framework reativo (ex: React, Vue, Angular) para garantir a responsividade (`RNF07`).
*   **Backend:** Linguagem de programação robusta (ex: Python/Django, Node.js/Express, Java/Spring) para implementar as APIs RESTful.
*   **Banco de Dados:** Solução relacional ou NoSQL para persistência de dados.

## Equipe de Desenvolvimento

O projeto Datefy está sendo desenvolvido pela seguinte equipe (Squad) [1]:

*   ANA
*   ANDRÉ
*   BÁRBARA
*   BRUNO
*   DAVID
*   EDU
*   LEONAN
*   LUCAS
*   LOHANNY
*   SIMÃO
*   RÉGIS

## Status do Projeto

*   **Tema:** Calendário Financeiro
*   **Prazo Estimado:** 07 de Dezembro de 2025
*   **Status Atual:** Fase de Especificação (Documentação de Requisitos e Casos de Uso)

## Cores da Marca

As cores oficiais da marca Datefy são [1]:

| Cor | Código Hexadecimal |
| :--- | :--- |
| Azul Escuro Principal | `#1B3C53` |
| Azul Secundário | `#234C6A` |
| Azul Claro/Cinzento | `#456882` |
| Bege/Off-White | `#D2C1B6` |

