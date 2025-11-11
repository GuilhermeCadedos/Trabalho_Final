<?php
$servername = "localhost";
$port = 3306;
$username = "root";
$password = "";
$dbname = "cadastro_checkup";
$table = "agendamentos";

$conn = new mysqli($servername, $username, $password, $dbname);

// Verifica a conexão
if ($conn->connect_error) {
    die("Erro na Conexão com o Banco de Dados: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    // Coleta e sanitiza os dados do POST
    
    $nome = $conn->real_escape_string($_POST['nome'] ?? '');
    $email = $conn->real_escape_string($_POST['email'] ?? '');
    $idade = (int) ($_POST['idade'] ?? 0); // Converte para inteiro
    $cpf = $conn->real_escape_string($_POST['cpf'] ?? '');
    // Cartão SUS é opcional
    $cartao_sus = $conn->real_escape_string($_POST['cartao_sus'] ?? NULL);
    $historico = $conn->real_escape_string($_POST['historico_familiar'] ?? 'nao');

    // Remove caracteres que não sejam números do CPF e Cartão SUS
    $cpf = preg_replace('/[^0-9]/', '', $cpf);
    if (!empty($cartao_sus)) {
        $cartao_sus = preg_replace('/[^0-9]/', '', $cartao_sus);
    }

    // Prepara a consulta SQL
    // Query SQL com placeholders (?) para segurança
    $sql = "INSERT INTO $table (nome, email, idade, cpf, cartao_sus, historico_familiar) VALUES (?, ?, ?, ?, ?, ?)";

    // Prepara a declaração (statement)
    if ($stmt = $conn->prepare($sql)) {

        // Liga as variáveis aos placeholders da query (Bind parameters)
        // O tipo dos dados deve ser especificado: s=string, i=integer, d=double
        // No nosso caso: s(nome), s(email), i(idade), s(cpf), s(cartao_sus), s(historico)
        $stmt->bind_param("ssisss", $nome, $email, $idade, $cpf, $cartao_sus, $historico);

        // Executa a declaração
        if ($stmt->execute()) {
            echo "<h2>✅ Inscrição Realizada com Sucesso!</h2>";
            echo "<p>Seu agendamento de interesse foi registrado. Entraremos em contato em breve.</p>";
            echo '<p><a href="cadastro.html">Voltar ao Formulário</a></p>';
        } else {
            // Verifica se o erro foi devido à duplicidade de CPF ou E-mail (chave UNIQUE)
            if ($conn->errno == 1062) {
                echo "<h2>❌ Erro ao Inserir Dados</h2>";
                echo "<p>Parece que você já se inscreveu. O CPF ou E-mail informado já está cadastrado.</p>";
            } else {
                echo "<h2>❌ Erro ao Inserir Dados</h2>";
                echo "<p>Ocorreu um erro ao registrar sua inscrição: " . $stmt->error . "</p>";
            }
        }

        // Fecha a declaração
        $stmt->close();

    } else {
        echo "<h2>❌ Erro de Preparação da Query</h2>";
        echo "<p>Ocorreu um erro na preparação da consulta: " . $conn->error . "</p>";
    }

} else {
    // Caso a página seja acessada diretamente sem o envio do formulário
    echo "<h2>Acesso Inválido</h2>";
    echo "<p>Por favor, envie o formulário através da página de cadastro.</p>";
}

// Fecha a conexão
$conn->close();