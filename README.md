Aqui está o README ajustado para o seu projeto:

# Chatbot de Voz Conversacional OpenAI

Este projeto é um chatbot com memória utilizando *Retrieval-Augmented Generation* (RAG) e integração de voz a partir de vídeos do YouTube, sendo apresentado no evento Conecta CEIA. Ele utiliza ferramentas avançadas de *speech-to-text* (STT) e *text-to-speech* (TTS), oferecendo uma experiência de interação por voz.

## Funcionalidades Principais:
- **Memória conversacional**: Utiliza *ConversationBufferMemory* para manter contexto durante as interações.
- **Carregamento de áudio do YouTube**: Usa o *YoutubeAudioLoader* para extrair e transcrever áudio de vídeos.
- **Transcrição de áudio**: Usa a API *Whisper-1* da OpenAI para transcrever áudio em texto.

## Estrutura do Projeto:
- `.streamlit/`: Configurações do Streamlit.
- `docs/`: Documentação do projeto.
- `.env`: Arquivo de variáveis de ambiente (inclui a chave API da OpenAI).
- `app.py`: Arquivo principal da aplicação em Streamlit.
- `docker-compose.yml`: Arquivo de configuração Docker Compose.
- `Dockerfile`: Dockerfile para configuração do ambiente Docker.
- `entrypoint.sh`: Script de entrada que executa o app.
- `generate_answer.py`: Lógica para geração de respostas.
- `helpers.py`: Funções auxiliares.
- `requirements.txt`: Lista de dependências.
- `README.md`: Este arquivo.

## Pré-requisitos:
- **Python 3.11** ou superior.
- Conta OpenAI com chave de API válida.
  
### Instalação sem Docker:

1. **Crie um ambiente virtual e instale as dependências:**
    ```bash
    python -m venv env
    source env/bin/activate  # Para Linux e MacOS
    # source env/Scripts/activate  # Para Windows
    pip install -r requirements.txt
    ```

2. **Adicione sua chave de API da OpenAI:**
   - Crie um arquivo `.env` na raiz do projeto e adicione:
     ```bash
     OPENAI_API_KEY=sk-xxxx
     ```

3. **Execute a aplicação:**
    ```bash
    streamlit run app.py
    ```

4. **Acesse o app:**
    O app será iniciado em `http://localhost:8501`.

### Execução com Docker:

1. **Configure o ambiente:**
   - Crie o arquivo `.env` com sua chave de API da OpenAI:
     ```bash
     OPENAI_API_KEY=sk-xxxx
     ```

2. **Execute os contêineres com Docker Compose:**
    ```bash
    sudo docker-compose up --build
    ```

3. **Acesse o app:**
    O app estará rodando em `http://localhost:8501`.

4. **Encerrar o contêiner:**
    Para parar e remover volumes:
    ```bash
    sudo docker-compose down -v
    ```

### Dockerfile:
O Dockerfile está configurado para criar um ambiente otimizado:
```Dockerfile
FROM python:3.11.5 AS chatbot

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
CMD ["sh", "entrypoint.sh"]
```

### docker-compose.yml:
```yaml
version: '3.8'
services:
  chatbot_api:
    container_name: chatbot_voice
    build:
      context: .
      dockerfile: Dockerfile
    env_file:
      - .env
    environment:
      - PYTHONPATH=/app
    ports:
      - "8501:8501"
    volumes:
      - ./:/app:rw
```

### Bibliotecas Utilizadas:
- **Streamlit** com *audio_recorder_streamlit*
- **ConversationBufferMemory** para manter o histórico de conversas
- **YoutubeAudioLoader** para extração de áudio de vídeos do YouTube
- **OpenAI Whisper** para transcrição de áudio:
  ```python
  transcript = OpenAI.audio.transcriptions.create(
      model="whisper-1",
      response_format="text",
      file=audio_file
  )
  ```

Esse projeto é uma ótima base para quem deseja explorar mais sobre integração de voz e inteligência artificial em chatbots.
