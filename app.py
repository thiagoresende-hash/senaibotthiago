#Segundo arquivo app.py
import streamlit as st
import chatbot as bot

st.set_page_config(page_title="SenaiBot", page_icon="🤖", layout="centered")


# Configuração inicial da página
st.title("🤖 SenaiBot")
st.caption("Implementação do projeto integrador entre tecnologias de I.A Generativa e Síntese de voz da Microsot")


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
            
#  ÁREA DE INTERAÇÃO
prompt = st.chat_input("Digite qualquer dúvida para o SenaiBot...")

if prompt:
    # 1. Exibir e guardar a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})

with st.sidebar:
    ##BOTÃO PARA RECONEHCER A FALA DO MICROFONE
    if st.button("🎤 Falar pelo microfone"):
        
        aviso = st.info("Estou ouvindo... Fale algo")
        
        texto_ouvido, resposta_ia = bot.conversar_por_voz(st.session_state.messages)
        
        aviso.empty()
        
    
    
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.messages = [
            {'role': 'system', 'content': 'Você é um professor assistente prestativo e conciso'}
        ]
        st.rerun()
    
    #2. Gerar a resposta do chatgpt
    with st.chat_message("assistant"):
        with st.spinner("Consultando o cérebro da IA...."):
            
            #Processamento da função de resposta da i.a
            resposta_chatbot = bot.obter_resposta_ia(st.session_state.messages)

            aviso.empty()


            
            st.markdown(resposta_chatbot)
