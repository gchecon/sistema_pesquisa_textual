import streamlit as st
import os
import psycopg2
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import openai
from llama_cpp import Llama
from rotinas import search_similar_documents

load_dotenv()

# Configurações
POSTGRESQL_URL = os.getenv('POSTGRESQL_URL')
MODEL_EMBEDDING = os.getenv('MODEL_EMBEDDING')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
LLAMA_MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'Llama3.1-70B'))

# Inicialização de modelos
embedding_model = SentenceTransformer(MODEL_EMBEDDING)
llama_model = Llama(model_path=LLAMA_MODEL_PATH)
openai.api_key = OPENAI_API_KEY

# Funções de banco de dados
def get_db_connection():
    return psycopg2.connect(POSTGRESQL_URL)

def save_prompt(name, content):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO prompts (name, content) VALUES (%s, %s)", (name, content))
        conn.commit()

def load_prompts():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT name, content FROM prompts")
            return cur.fetchall()

# Funções de LLM
def generate_openai_response(prompt, context):
    full_prompt = context + "\n\n" + prompt
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=full_prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def generate_llama_response(prompt, context):
    full_prompt = context + "\n\n" + prompt
    response = llama_model(full_prompt, max_tokens=150)
    return response['choices'][0]['text'].strip()

# Interface Streamlit
st.title("LLM Chat Interface")

# Sidebar para seleção de LLM e gerenciamento de prompts
st.sidebar.header("Configurações")

# Seleção de LLM
llm_choice = st.sidebar.radio("Escolha a LLM:", ("OpenAI", "Llama 3"))

# Gerenciamento de prompts
st.sidebar.header("Gerenciamento de Prompts")
prompt_action = st.sidebar.radio("Ação:", ("Carregar Prompt", "Criar Novo Prompt"))

if prompt_action == "Carregar Prompt":
    prompts = load_prompts()
    selected_prompt = st.sidebar.selectbox("Selecione um prompt:", [p[0] for p in prompts])
    if selected_prompt:
        prompt_content = next(p[1] for p in prompts if p[0] == selected_prompt)
        st.sidebar.text_area("Conteúdo do Prompt:", value=prompt_content, height=200)
else:
    new_prompt_name = st.sidebar.text_input("Nome do novo prompt:")
    new_prompt_content = st.sidebar.text_area("Conteúdo do novo prompt:", height=200)
    if st.sidebar.button("Salvar Prompt"):
        save_prompt(new_prompt_name, new_prompt_content)
        st.sidebar.success("Prompt salvo com sucesso!")

# Chat principal
st.header("Chat")

# Inicializar histórico de chat se não existir
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Exibir histórico de chat
for message in st.session_state.chat_history:
    st.text(message)

# Input do usuário
user_input = st.text_input("Digite sua mensagem:")

if st.button("Enviar"):
    # Adicionar input do usuário ao histórico
    st.session_state.chat_history.append(f"Você: {user_input}")

    # Gerar contexto baseado no histórico recente
    context = "\n".join(st.session_state.chat_history[-5:])  # Últimas 5 mensagens

    # Gerar resposta baseada na LLM selecionada
    if llm_choice == "OpenAI":
        response = generate_openai_response(user_input, context)
    else:
        response = generate_llama_response(user_input, context)

    # Adicionar resposta ao histórico
    st.session_state.chat_history.append(f"LLM: {response}")

    # Atualizar a exibição
    st.experimental_rerun()

# Busca de documentos similares
st.header("Busca de Documentos Similares")
search_query = st.text_input("Digite sua consulta para buscar documentos similares:")
if st.button("Buscar"):
    similar_docs = search_similar_documents(search_query, embedding_model)
    st.write("Documentos similares encontrados:")
    for doc, score in similar_docs:
        st.write(f"- {doc} (Similaridade: {score:.2f})")