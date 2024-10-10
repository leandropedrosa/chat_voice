Aqui está a versão ajustada e traduzida para português do seu README:

# Chatbot de Voz Conversacional OpenAI

Neste discurso técnico, embarco em uma exploração das capacidades avançadas de *text-to-speech (TTS)* e *speech-to-text (STT)* da OpenAI. Essas inovações estão revolucionando as dinâmicas de interação entre humanos e máquinas, além de abrir novos caminhos para acessibilidade e eficiência. Se você é um desenvolvedor experiente, um entusiasta de tecnologia, ou simplesmente curioso sobre os avanços na vanguarda da IA, esta implementação pode ser usada como um protótipo para projetos mais sofisticados que utilizem as funcionalidades de TTS e STT.

## Uso
Para usar este aplicativo, siga os seguintes passos:

- É recomendado ter o **Python 3.10** ou superior.
- Crie um ambiente virtual e instale os requisitos.

    Navegue até o diretório do projeto, crie um ambiente virtual usando o comando:
    ```py
    python -m venv env
    ```
    E ative-o usando o comando:
    ```py
    - source env/Scripts/activate   # Para Windows, utilizando o Git Bash
    - source env/bin/activate       # Para Linux e OSX
    ```

## Uso com Streamlit
Após concluir os passos anteriores, é hora de conversar. Siga os passos abaixo, por favor:

1. Crie um arquivo **.env** e cole nele sua *OPENAI_API_KEY*. O conteúdo do **.env** deve ser semelhante a:
    ```py
    OPENAI_API_KEY=sk-xxxx
    ```
    que deve ter um total de 51 caracteres.

2. Crie um diretório **.streamlit/secrets.toml** e cole nele sua *OPENAI_API_KEY*. O conteúdo do **secrets.toml** deve ser semelhante a:
    ```py
    # .streamlit/secrets.toml

    [passwords]
    # Siga a regra: username = "password"
    username = "sk-xxxx"
    ```
    que deve ter um total de 51 caracteres. Além disso, a palavra *username* pode ser alterada, representando o nome de usuário escolhido para inserir no app do Streamlit, junto com a *OPENAI_API_KEY*.

3. Execute o app usando o comando:
    ```py
    streamlit run app.py    # Ou, para selecionar uma porta, você pode usar o comando:
    streamlit run app.py --server.port=85XX
    ```

4. De acordo com as configurações, abra um navegador e o app deve estar rodando em:
    ```py
        http://localhost:85XX/          # ou
        http://127.0.0.1:85XX/          
    ```
    Observe que mesmo sem especificar o IP e a porta no app, esses valores serão definidos como padrão.

5. Insira suas credenciais:
    ```py
    username=username               # Use a string: username (definida no script, pode ser ajustada)
    password=YOUR_OPENAI_API_KEY     # Igual àquela que existe no arquivo .env
    ```