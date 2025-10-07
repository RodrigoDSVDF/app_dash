
# Use uma imagem base Python oficial
FROM python:3.9-slim-buster

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o arquivo requirements.txt e instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação para o diretório de trabalho
COPY .

# Expor a porta em que o Dash será executado
EXPOSE 8050

# Comando para executar o aplicativo Dash
CMD ["python", "dash_app.py"]

