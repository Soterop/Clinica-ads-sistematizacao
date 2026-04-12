from app import app

if __name__ == "__main__":
    # debug=True permite que o servidor reinicie sozinho ao salvar alterações no código
    # host='0.0.0.0' é fundamental para que o Docker consiga mapear a porta corretamente
    app.run(host='0.0.0.0', port=5000, debug=True)