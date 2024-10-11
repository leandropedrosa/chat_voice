# Etapa de instalação das dependências
FROM python:3.11.5 AS chatbot

# Configura o diretório de trabalho
WORKDIR /app

# Atualiza pacotes e instala o ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copia apenas os arquivos essenciais
COPY requirements.txt /app/

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do projeto
COPY . /app

# Configura a entrada para rodar o app
CMD ["sh", "entrypoint.sh"]