let subtemasSelecionados = {
    tema: null,
    modelo: null,
    verbosidade: null
};

// Funções para abrir os submenus ao clicar
document.getElementById('tema-menu').addEventListener('click', function() {
    toggleSubmenu('tema-submenu');
});
document.getElementById('modelo-menu').addEventListener('click', function() {
    toggleSubmenu('modelo-submenu');
});
document.getElementById('verbosidade-menu').addEventListener('click', function() {
    toggleSubmenu('verbosidade-submenu');
});

function toggleSubmenu(id) {
    const submenu = document.getElementById(id);
    submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';
}

// Lógica para selecionar subtemas
document.querySelectorAll('.subtema-option').forEach(item => {
    item.addEventListener('click', function() {
        const subtema = this.innerText;

        // Verifica qual submenu está sendo selecionado
        if (this.closest('#tema-submenu')) {
            subtemasSelecionados.tema = subtema;
        } else if (this.closest('#modelo-submenu')) {
            subtemasSelecionados.modelo = subtema;
        } else if (this.closest('#verbosidade-submenu')) {
            subtemasSelecionados.verbosidade = subtema;
        }

        // Atualiza a área de subtemas escolhidos
        atualizarSubtemasEscolhidos();

        // Verifica se os três submenus foram selecionados
        if (subtemasSelecionados.tema && subtemasSelecionados.modelo && subtemasSelecionados.verbosidade) {
            document.getElementById('start-button').classList.remove('disabled');
            document.getElementById('error-message').style.display = 'none'; // Oculta a mensagem de erro se já foi exibida
        }
    });
});

function atualizarSubtemasEscolhidos() {
    const chosenSubjectsDiv = document.getElementById('subtema-selecionado');
    chosenSubjectsDiv.innerHTML = `
        <div>Tema: ${subtemasSelecionados.tema || ''}</div>
        <div>Modelo: ${subtemasSelecionados.modelo || ''}</div>
        <div>Verbosidade: ${subtemasSelecionados.verbosidade || ''}</div>
    `;
}

// Lógica para iniciar a interação
document.getElementById('start-button').addEventListener('click', function() {
    if (subtemasSelecionados.tema && subtemasSelecionados.modelo && subtemasSelecionados.verbosidade) {
        // Esconde o logo e mostra a área de prompts
        document.getElementById('main-logo').style.display = 'none';
        document.getElementById('prompt-area').style.display = 'block';
        document.getElementById('error-message').style.display = 'none';
    } else {
        // Exibe a mensagem de erro se os submenus não forem selecionados
        document.getElementById('error-message').style.display = 'block';
    }
});

// Lógica para enviar o prompt
document.getElementById('send-prompt').addEventListener('click', function() {
    const prompt = document.getElementById('prompt-input').value;
    fetch('/process_prompt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt })
    })
    .then(response => response.json())
    .then(data => {
        const responseArea = document.getElementById('response-area');
        responseArea.innerHTML += `<div><strong>Prompt:</strong> ${prompt}</div>`;
        responseArea.innerHTML += `<div><strong>Resposta:</strong> ${data.response}</div>`;
    });
});