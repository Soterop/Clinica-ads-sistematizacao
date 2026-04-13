# Imagem base do Python
FROM python:3.10-slim

# Instala dependências do sistema para o PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /app

# Instala dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copia o restante do código
COPY . .


# Comando para rodar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
