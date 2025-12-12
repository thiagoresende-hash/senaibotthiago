# Segundo arquivo app.py
import streamlit as st
import chatbot as bot

st.set_page_config(page_title="SenaiBot", page_icon="🤖", layout="centered")

# Configuração inicial da página
st.title("🤖 SenaiBot")
st.caption("Implementação do projeto integrador entre tecnologias de I.A Generativa e Síntese de voz da Microsoft")

# Inicialização da memória (cache)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {'role': 'system', 'content': "Você é um professor assistente prestativo e conciso"}
    ]

# RENDERIZAR AS MENSAGENS ANTIGAS
for msg in st.session_state.messages:
    if msg['role'] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg['content'])

# ÁREA DE INTERAÇÃO
prompt = st.chat_input("Digite qualquer dúvida para o SenaiBot...")

if prompt:
    # 1. Exibir e guardar a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})

# SIDEBAR
with st.sidebar:
    # BOTÃO PARA RECONHECER A FALA DO MICROFONE
    if st.button("🎤 Falar pelo microfone"):
        aviso = st.info("Estou ouvindo... Fale algo")

        texto_ouvido, resposta_ia = bot.conversar_por_voz(st.session_state.messages)

        aviso.empty()  # aqui funciona porque 'aviso' foi definido acima

    # BOTÃO PARA LIMPAR CONVERSA