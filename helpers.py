import base64
import streamlit as st
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Inicializa o cliente OpenAI com a chave da API
client = OpenAI(api_key=api_key)
openai.api_key = api_key

def speech_to_text(audio_data):
    """Converte áudio para texto usando o modelo Whisper da OpenAI."""
    try:
        with open(audio_data, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                response_format="text",
                file=audio_file
            )
        return transcript
    except openai.APIError as e:
        return ""
    except openai.APIConnectionError as e:
        raise ValueError("Não há coneção com a OPENAI neste momento. Por favor, tente mais tarde.")
    except openai.RateLimitError as e:
        raise ValueError("Limite de requisições alcançadas. Por favor, tente mais tarde.")

def text_to_speech(input_text):
    """Converte texto para áudio usando o modelo de Text-to-Speech da OpenAI."""
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    # Salva o áudio gerado em um arquivo MP3
    caminho_arquivo_audio = "temp_audio_play.mp3"
    with open(caminho_arquivo_audio, "wb") as f:
        response.stream_to_file(caminho_arquivo_audio)
    return caminho_arquivo_audio


def autoplay_audio(file_path: str):
    """Reproduz automaticamente um arquivo de áudio na interface Streamlit."""
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)
