const CHATBOT_API_URL = "http://127.0.0.1:5000/chatbot";

document.addEventListener("DOMContentLoaded", () => {
  const chatBubble = document.getElementById("chat-bubble");
  const chatWindow = document.getElementById("chat-window");
  const chatMessages = document.getElementById("chat-messages");
  const chatInput = document.getElementById("chat-input");
  const chatSendBtn = document.getElementById("chat-send-btn");
  const chatCloseBtn = document.getElementById("chat-close-btn");

  let initialMessageSent = false;

  // Abrir Chat
  chatBubble.addEventListener("click", () => {
    chatWindow.classList.add("active");
    chatBubble.style.display = "none";

    if (!initialMessageSent) {
      addBotMessage(
        "Olá! Sou o Chatbot do Novembro Azul. Pergunte sobre sintomas, prevenção ou check-ups."
      );
      initialMessageSent = true;
    }
    chatInput.focus();
  });

  // Fechar Chat
  chatCloseBtn.addEventListener("click", () => {
    chatWindow.classList.remove("active");
    chatBubble.style.display = "flex";
  });

  // Adicionar Mensagem
  function addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("chat-message", `${sender}-message`);
    messageDiv.innerHTML = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function addUserMessage(text) {
    addMessage(text, "user");
  }

  function addBotMessage(text) {
    addMessage(text, "bot");
  }

  // Enviar Mensagem
  async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    chatInput.value = "";
    addUserMessage(message);

    // Indicador de digitação
    const typingIndicator = document.createElement("div");
    typingIndicator.classList.add(
      "chat-message",
      "bot-message",
      "typing-indicator"
    );
    typingIndicator.textContent = "Digitando...";
    chatMessages.appendChild(typingIndicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
      const response = await fetch(CHATBOT_API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP ${response.status}`);
      }

      const data = await response.json();
      typingIndicator.remove();
      addBotMessage(data.response);
    } catch (error) {
      console.error(error);
      typingIndicator.remove();
      addBotMessage("❌ Erro de conexão. Tente novamente.");
    }
  }

  // Eventos de Envio
  chatSendBtn.addEventListener("click", sendMessage);
  chatInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      sendMessage();
    }
  });
});
