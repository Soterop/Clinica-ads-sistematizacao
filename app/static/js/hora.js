function atualizarInterface() {
    const agora = new Date();
    
    // 1. Atualizar o Relógio
    const horas = String(agora.getHours()).padStart(2, '0');
    const minutos = String(agora.getMinutes()).padStart(2, '0');
    const segundos = String(agora.getSeconds()).padStart(2, '0');
    
    const relogioFormatado = `${horas}:${minutos}:${segundos}`;
    document.getElementById('relogio').innerText = relogioFormatado;

    // 2. Lógica de Saudação (Executa apenas uma vez ou a cada hora)
    const horaAtual = agora.getHours();
    let saudacao = "";

    if (horaAtual >= 5 && horaAtual < 12) {
        saudacao = "Bom dia!";
    } else if (horaAtual >= 12 && horaAtual < 18) {
        saudacao = "Boa tarde!";
    } else {
        saudacao = "Boa noite!";
    }

    const elementoSaudacao = document.getElementById('mensagem-saudacao');
    if (elementoSaudacao.innerText !== saudacao) {
        elementoSaudacao.innerText = saudacao;
    }
}

// Executa a função a cada 1 segundo (1000 milissegundos)
setInterval(atualizarInterface, 1000);

// Chama uma vez ao carregar para não esperar 1 segundo para aparecer
atualizarInterface();