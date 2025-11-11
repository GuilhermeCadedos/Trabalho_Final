const toggleButton = document.getElementById('theme-toggle');
const body = document.body;
const iconSpan = document.getElementById('theme-icon'); // Usando o ID do span para o emoji

// 1. Função para aplicar o tema
function applyTheme(theme) {
  if (theme === 'dark') {
    body.classList.add('dark-mode');
    iconSpan.textContent = '☀️'; // Sol para o tema escuro (pedir o tema claro)
    toggleButton.setAttribute('aria-checked', 'true');
  } else {
    body.classList.remove('dark-mode');
    iconSpan.textContent = '🌙'; // Lua para o tema claro (pedir o tema escuro)
    toggleButton.setAttribute('aria-checked', 'false');
  }
  // Salva a preferência no armazenamento local (localStorage)
  localStorage.setItem('theme', theme);
}

// 2. Tenta carregar a preferência salva ou usa o padrão do sistema
const savedTheme = localStorage.getItem('theme');

// Verifica a preferência do sistema, mas apenas se não houver um tema salvo
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

if (savedTheme) {
  applyTheme(savedTheme);
} else if (prefersDark) {
  applyTheme('dark');
} else {
  applyTheme('light');
}

// 3. Evento para alternar o tema ao clicar no botão
toggleButton.addEventListener('click', () => {
  const currentTheme = body.classList.contains('dark-mode') ? 'dark' : 'light';
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  applyTheme(newTheme);
});