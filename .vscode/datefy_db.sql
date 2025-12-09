CREATE DATABASE IF NOT EXISTS `DATEFY_db`
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `DATEFY_db`;

-- -------------------------------------------------------------------------
-- 2. CRIAÇÃO DAS TABELAS
-- -------------------------------------------------------------------------

-- Tabela 'usuarios'
-- Contém dados de autenticação e identificação do usuário.
CREATE TABLE IF NOT EXISTS `usuarios` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `nome` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) UNIQUE NOT NULL COMMENT 'E-mail deve ser único para login',
    `senha_hash` VARCHAR(255) NOT NULL COMMENT 'Armazena a senha criptografada (hash)'
) ENGINE=InnoDB;

-- Tabela 'tarefas'
-- Gerencia as tarefas pessoais dos usuários.
CREATE TABLE IF NOT EXISTS `tarefas` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `titulo` VARCHAR(255) NOT NULL,
    `descricao` TEXT COMMENT 'Descrição detalhada da tarefa',
    `data` VARCHAR(10) NOT NULL COMMENT 'Data da tarefa (formato YYYY-MM-DD ou similar)',
    `categoria` VARCHAR(50) COMMENT 'Categoria ou tag da tarefa',
    `status` TINYINT DEFAULT 0 COMMENT '0: pendente, 1: concluída',
   
    -- Chave estrangeira que conecta a tarefa ao usuário
    FOREIGN KEY (`user_id`) REFERENCES `usuarios`(`id`)
        ON DELETE CASCADE -- Se o usuário for deletado, suas tarefas também serão
) ENGINE=InnoDB;

-- Tabela 'financas'
-- Gerencia os registros de receitas e despesas.
CREATE TABLE IF NOT EXISTS `financas` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `usuario_id` INT NOT NULL,
    `descricao` VARCHAR(255) COMMENT 'Breve descrição da transação',
    `categoria` VARCHAR(50) COMMENT 'Categoria da transação (ex: salario, mercado, lazer)',
    `tipo` VARCHAR(10) NOT NULL COMMENT 'Tipo de transação: "entrada" ou "saida"',
    `valor` FLOAT NOT NULL COMMENT 'Valor da transação',
    `forma_pagamento` VARCHAR(50) COMMENT 'Forma de pagamento (ex: credito, debito, pix)',
    `parcelas` INT DEFAULT 1 COMMENT 'Número de parcelas (para compras parceladas)',
    `data` VARCHAR(10) COMMENT 'Data da transação (formato YYYY-MM-DD ou similar)',
   
    -- Chave estrangeira que conecta a transação ao usuário
    FOREIGN KEY(`usuario_id`) REFERENCES `usuarios`(`id`)
        ON DELETE CASCADE -- Se o usuário for deletado, suas finanças também serão
) ENGINE=InnoDB;

-- -------------------------------------------------------------------------
-- 3. CRIAÇÃO DE USUÁRIO E PERMISSÕES (Opcional, mas recomendado)
-- Você pode pular esta seção se já tiver um usuário com permissões.
-- -------------------------------------------------------------------------

-- Altere 'app_user' e 'senha_forte_aqui' para credenciais seguras.
-- CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'senha_forte_aqui';
-- GRANT ALL PRIVILEGES ON minha_aplicacao_db.* TO 'app_user'@'localhost';
-- FLUSH PRIVILEGES;

-- -------------------------------------------------------------------------
-- 4. ÍNDICES (Opcional, mas melhora performance)
-- -------------------------------------------------------------------------

-- Índice para a busca de tarefas por usuário e status
CREATE INDEX idx_tarefas_user_status ON tarefas (user_id, status);

-- Índice para a busca de finanças por usuário e data (comum para relatórios)
CREATE INDEX idx_financas_user_data ON financas (usuario_id, data DESC);