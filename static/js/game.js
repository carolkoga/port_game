let currentChallengeId = null;

// --- FUNÇÃO 1: BUSCAR NOVO DESAFIO ---
async function nextChallenge() {
    // 1. Limpa a tela do desafio anterior
    document.getElementById('result-details').style.display = 'none'; // Esconde a caixa de detalhes
    document.getElementById('feedback').innerText = '';             // Limpa a mensagem de erro/acerto
    document.getElementById('user-input').value = '';               // Limpa o input
    document.getElementById('user-input').focus();                  // Coloca o cursor no input automaticamente

    // 2. Busca dados no Backend
    try {
        const response = await fetch('/get_challenge');

        if (!response.ok) throw new Error('Erro ao buscar desafio');

        const data = await response.json();

        // 3. Atualiza a tela com a nova porta
        currentChallengeId = data.id;
        document.getElementById('port-num').innerText = data.porta;
    } catch (error) {
        console.error("Erro:", error);
        document.getElementById('feedback').innerText = "Erro ao conectar com o servidor.";
    }
}

// --- FUNÇÃO 2: VERIFICAR RESPOSTA (ENTER) ---
document.getElementById('user-input').addEventListener('keypress', async (e) => {
    if (e.key === 'Enter') {
        // Previne envio duplo se o usuário apertar Enter várias vezes rápido
        if (document.getElementById('feedback').innerText !== '') return;

        const input = e.target.value.toUpperCase().trim();

        // Envia resposta para o Python
        const response = await fetch('/check_answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: currentChallengeId, sigla: input })
        });

        const result = await response.json();
        const feedbackEl = document.getElementById('feedback');

        // --- ATUALIZAÇÃO DA INTERFACE ---

        // 1. Mostra Score e Mensagem Principal
        feedbackEl.innerText = result.message;
        document.getElementById('score-val').innerText = result.new_score;

        if (result.correct) {
            feedbackEl.style.color = "#00ff41"; // Verde Matrix
        } else {
            feedbackEl.style.color = "#ff4444"; // Vermelho Alerta
        }

        // 2. Preenche a Caixa de Detalhes (A parte educativa!)
        // Agora isso roda TANTO no acerto QUANTO no erro
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

            // Exibe a caixa verde com as infos
            document.getElementById('result-details').style.display = 'block';
        }

        // 3. Temporizador inteligente
        // Se acertou: espera 4 segundos. Se errou: espera 6 segundos (para dar tempo de ler).
        const delayTime = result.correct ? 20000 : 60000;
        setTimeout(nextChallenge, delayTime);
    }
});

nextChallenge();