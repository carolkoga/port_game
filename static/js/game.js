let currentChallengeId = null;
let isWaitingNext = false; // Controle para saber se estamos esperando o usuário avançar

// --- FUNÇÃO 1: BUSCAR NOVO DESAFIO ---
async function nextChallenge() {
    // 1. Reseta a interface para o estado inicial
    isWaitingNext = false;
    document.getElementById('result-details').style.display = 'none';
    document.getElementById('feedback').innerText = '';
    document.getElementById('next-btn').style.display = 'none'; // Esconde o botão

    // 2. Destrava e limpa o input
    const inputEl = document.getElementById('user-input');
    inputEl.value = '';
    inputEl.disabled = false;
    inputEl.focus();

    // 3. Busca dados no Backend
    try {
        const response = await fetch('/get_challenge');
        if (!response.ok) throw new Error('Erro ao buscar desafio');

        const data = await response.json();

        currentChallengeId = data.id;
        document.getElementById('port-num').innerText = data.porta;
    } catch (error) {
        console.error("Erro:", error);
        document.getElementById('feedback').innerText = "Erro ao conectar com o servidor.";
    }
}

// --- FUNÇÃO 2: CONTROLADOR DE EVENTOS (ENTER) ---
document.getElementById('user-input').addEventListener('keypress', async (e) => {
    // Se apertar Enter, mas já tiver respondido, funciona como clicar no botão "Próximo"
    if (e.key === 'Enter' && isWaitingNext) {
        nextChallenge();
        return;
    }

    if (e.key === 'Enter' && !isWaitingNext) {
        const inputEl = e.target;
        const inputVal = inputEl.value.toUpperCase().trim();

        // Evita envio vazio
        if (!inputVal) return;

        // Trava o input para não editar enquanto processa
        inputEl.disabled = true;

        const response = await fetch('/check_answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentChallengeId, sigla: inputVal })
        });

        const result = await response.json();
        const feedbackEl = document.getElementById('feedback');

        // --- EXIBE RESULTADO ---
        feedbackEl.innerText = result.message;
        document.getElementById('score-val').innerText = result.new_score;

        if (result.correct) {
            feedbackEl.style.color = "#00ff41";
        } else {
            feedbackEl.style.color = "#ff4444";
        }

        // --- EXIBE DETALHES TÉCNICOS ---
        if (result.details) {
            const details = result.details;
            document.getElementById('det-desc').innerText = details.descricao;
            document.getElementById('det-cat').innerText = details.categoria;

            const statusEl = document.getElementById('det-status');
            if (details.segura) {
                statusEl.innerText = "🛡️ SEGURO (Criptografado / Recomendado)";
                statusEl.style.color = "#00ff41";
            } else {
                statusEl.innerText = "⚠️ INSEGURO (Texto claro / Legado)";
                statusEl.style.color = "#ff4444";
            }
            document.getElementById('result-details').style.display = 'block';
        }

        // --- FINALIZA O TURNO ---
        // Mostra o botão para avançar manualmente
        document.getElementById('next-btn').style.display = 'inline-block';
        isWaitingNext = true;

        // Foca no botão para facilitar apertar Enter de novo
        document.getElementById('next-btn').focus();
    }
});

// Evento de clique no botão (caso use o mouse)
document.getElementById('next-btn').addEventListener('click', nextChallenge);

// Inicia o jogo
nextChallenge();