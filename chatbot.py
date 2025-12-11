import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import azure.cognitiveservices.speech as speech_sdk

# Carrega automaticamente variáveis do .env
load_dotenv()


# ===============================
# CONFIGURAÇÃO DO CLIENTE OPENAI
# ===============================
def configurar_cliente_openai():
    """Inicializa e retorna o cliente da Azure OpenAI."""
    try:
        return AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OAI_KEY"),
            api_version="2024-02-15-preview"
        )
    except Exception as e:
        print(f"Erro ao configurar OpenAI: {e}")
        return None
    

# ===============================
# FUNÇÃO DE SÍNTESE DE FALA
# ===============================
def falar_texto(texto: str) -> bool:
    """
    Recebe uma string e a reproduz nos alto-falantes.
    Retorna True se funcionou, False se falhou.
    """
    try:
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")

        if not speech_key or not speech_region:
            print("Chaves de fala não encontradas.")
            return False

        # Configuração do serviço de fala
        speech_config = speech_sdk.SpeechConfig(subscription=speech_key, region=speech_region)

        # Escolha da voz (pode trocar por outras vozes disponíveis no Azure)
        speech_config.speech_synthesis_voice_name = "pt-BR-FranciscaNeural"

        # Saída de áudio: alto-falante padrão
        audio_config = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)

        # Criação do sintetizador
        synthesizer = speech_sdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        # Executa a fala (aguarda terminar)
        result = synthesizer.speak_text_async(texto).get()

        if result.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
            return True
        else:
            print(f"Erro na síntese de fala: {result.reason}")
            return False

    except Exception as e:
        print(f"Erro ao falar: {e}")
        return False


# ===============================
# OBTÉM RESPOSTA DA IA
# ===============================
def obter_resposta_ia(mensagens_historico):
    """
    Recebe o histórico de conversa (lista de dicts)
    e retorna a resposta da IA (string).
    """
    client = configurar_cliente_openai()

    if not client:
        return "Erro de conexão com a IA."

    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OAI_DEPLOYMENT"),
            messages=mensagens_historico,
            temperature=1.0,
            max_tokens=5000,
        )

        resposta_texto = response.choices[0].message.content

        # 🔊 Fala a resposta usando Azure Speech
        falar_texto(resposta_texto)

        return resposta_texto

    except Exception as e:
        return f"Desculpe, tive um erro técnico: {str(e)}"






# ===============================
# RECONHECIMENTO DE FALA
# ===============================
speech_config = None

def configurar_reconhecimento_fala():
    global speech_config
    
    try:
        speech_key  = os.getenv("AZURE_SPEECH_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")
        
        speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)
        speech_config.speech_recognition_language = 'pt-BR'
        
    except Exception as e:
        print(f"Erro ao configurar o serviço de reconhecimento de fala: {e}")

# ========================
# RECONHECER FALA DO MICROFONE
# ========================

def ouvir_microfone():
    global speech_config
    
    if speech_config is None:
        configurar_reconhecimento_fala()
        
    recognizer = speech_sdk.SpeechRecognizer(
        speech_config,
        audio_config=speech_sdk.AudioConfig(use_default_microphone=True)
    )
    
    print("Fale agora...")
    
    result = recognizer.recognize_once_async().get()
    
    if result.reason == speech_sdk.ResultReason.RecognizedSpeech:
        return result.text
    
    elif result.reson == speech_sdk.ResultReason.NoMatch:
        print("Não entendi o que foi DITO!")
        return ""
    
    else:
        print("Erro no reconhecimento da voz: ", result.reason)
        return ""

#=============================
# FUNÇÃO COMPLETA
#=============================
def conversar_por_voz(mensagens_historico):
    """
        1. Ouvir o mic
        2. Converter a fala em texto
        3. Enviar para o gpt
        4. fala a resposta
        5. voz sintetizada
    """
    
    texto_ouvido = ouvir_microfone()
    
    if not texto_ouvido:
        return "", "Não consegui entender a sua fala!"
    
    mensagens_historico.append({'role': "user", "content": texto_ouvido})
    
    resposta_ia = obter_resposta_ia(mensagens_historico)
    
    falar_texto(resposta_ia)
    
    return texto_ouvido, resposta_ia
