# Imagem base do Python
FROM python:3.10-slim

# Instala dependências do sistema para o PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "run.py"]
