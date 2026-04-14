
document.querySelector('form').addEventListener('submit', function() {
    let cpfInput = this.querySelector('input[name="cpf"]');
    if (cpfInput) {
        cpfInput.value = cpfInput.value.replace(/\D/g, ''); // Remove tudo que não é número
    }
});