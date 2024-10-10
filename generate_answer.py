import os
from glob import glob


import openai
from openai import OpenAI
from dotenv import load_dotenv
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Inicializa o cliente OpenAI
client = OpenAI(api_key=api_key)
openai.api_key = api_key


def base_model_chatbot(messages):
    """Função principal para interagir com o chatbot baseado no modelo GPT-3.5."""
    system_message = [
        {"role": "system", "content": "Você é um chatbot de IA útil, que responde a perguntas feitas pelo Usuário."}
    ]
    messages = system_message + messages
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )
    return response.choices[0].message.content


class VectorDB:
    """Classe para gerenciar o carregamento de documentos e criação de banco de dados vetorial."""

    def __init__(self, docs_directory: str):
        self.docs_directory = docs_directory

    def create_vector_db(self):
        """Função para criar o banco de dados vetorial a partir de documentos PDF."""
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

        # Carrega todos os arquivos PDF do diretório especificado
        files = glob(os.path.join(self.docs_directory, "*.pdf"))

        # Carrega os PDFs usando o PyPDFLoader
        loadPDFs = [PyPDFLoader(pdf_file) for pdf_file in files]

        pdf_docs = list()
        for loader in loadPDFs:
            pdf_docs.extend(loader.load())

        # Divide os documentos em partes menores (chunks) para processamento
        chunks = text_splitter.split_documents(pdf_docs)

        # Cria e retorna o banco de dados vetorial usando as embeddings da OpenAI
        return Chroma.from_documents(chunks, OpenAIEmbeddings())

    def load_youtube_vector_db(self):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        loader = GenericLoader(
            YoutubeAudioLoader(
                ["https://www.youtube.com/watch?v=gsDnrHtUabY"],
                "docs/youtube/"),
            OpenAIWhisperParser()
        )

        # Carrega os documentos do vídeo
        video_docs = loader.load()

        if not video_docs:
            raise ValueError("Nenhum documento foi carregado do vídeo do YouTube.")

        # Divide os documentos em chunks
        chunks = text_splitter.split_documents(video_docs)

        if not chunks:
            raise ValueError("Os chunks do vídeo estão vazios.")

        print(f"Documentos carregados: {video_docs}")
        print(f"Chunks gerados: {chunks}")

        # Cria e retorna o banco de dados vetorial
        return Chroma.from_documents(chunks, OpenAIEmbeddings())

class ConversationalRetrievalChain:
    """Classe para gerenciar a configuração da cadeia de perguntas e respostas (QA)."""

    def __init__(self, model_name="gpt-3.5-turbo", temperature=0):
        self.model_name = model_name
        self.temperature = temperature

    def create_chain(self):
        """Cria a cadeia de perguntas e respostas usando o modelo especificado e a memória de conversação."""

        model = ChatOpenAI(
            model_name=self.model_name,
            temperature=self.temperature,
        )

        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # Cria o banco de dados vetorial com base nos documentos da pasta 'docs/'
        vector_db = VectorDB('docs/')
        retriever = vector_db.load_youtube_vector_db().as_retriever(
            search_type="similarity",
            search_kwargs={"k": 2},
        )

        # Retorna a cadeia de QA usando o modelo, o recuperador e a memória
        return RetrievalQA.from_chain_type(
            llm=model,
            retriever=retriever,
            memory=memory,
        )


def with_pdf_chatbot(messages):
    """Função principal para executar o sistema de perguntas e respostas com PDFs."""
    query = messages[-1]['content'].strip()  # Extrai a última mensagem do usuário

    # Cria a cadeia de QA
    qa_chain = ConversationalRetrievalChain().create_chain()
    result = qa_chain({"query": query})  # Executa a consulta no QA
    return result['result']  # Retorna o resultado da resposta
