-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 09/11/2025 às 17:06
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `cadastro_checkup`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `agendamentos`
--

CREATE TABLE `agendamentos` (
  `id` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `idade` int(11) NOT NULL,
  `cpf` varchar(11) NOT NULL,
  `cartao_sus` varchar(15) DEFAULT NULL,
  `historico_familiar` enum('nao','sim','nao_sei') NOT NULL DEFAULT 'nao',
  `data_inscricao` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `agendamentos`
--

INSERT INTO `agendamentos` (`id`, `nome`, `email`, `idade`, `cpf`, `cartao_sus`, `historico_familiar`, `data_inscricao`) VALUES
(1, 'Gabriela Ambrósio Mariano', 'gabriela_teste@teste.com', 28, '148987498', '15450484890', 'nao', '2025-11-09 03:49:07'),
(2, 'Paulo Roberto', 'paulo_test@teste.com', 85, '58844785995', '27878262', 'sim', '2025-11-09 06:21:54'),
(3, 'José da Silva', 'jose_teste@teste.com', 45, '4654654678', '45454545', 'sim', '2025-11-09 13:53:31');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `agendamentos`
--
ALTER TABLE `agendamentos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `cpf` (`cpf`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `agendamentos`
--
ALTER TABLE `agendamentos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
