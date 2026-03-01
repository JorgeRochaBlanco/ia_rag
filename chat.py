from dotenv import load_dotenv
import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader

from app.agent_investigacion import InvestigationAgent


##############################################################
# Funciones auxiliares
# Función para resetear el chat
def reset_conversation():
  st.session_state.conversation = None
  st.session_state.chat_history = None
  st.session_state.messages = []

# Funciones para convertir a texto la cadena de preguntas y respuestas generadas en el chat
def get_txt_messages(messages):
    return "\n".join([item["role"]+": "+(item["content"] if item["content"] else "")+"\n" for item in messages])


################################################################
# Secretos a través de streamlit secrets
instructions_ia = InvestigationAgent.load_instructions(st.secrets["FICH_INSTRUCCIONES_IA"])
print("Modelo IA a usar:", end="\t")
modelo_ia = st.secrets["IA_MODEL"]
print(modelo_ia)
print("Nombre de Storage Google: ", end="\t")
print(st.secrets["STORE_NAME"])
print("API Key: ", end="\t")
print(st.secrets["GEMINI_API_KEY"])
print("Instrucciones para el agente:")
print(instructions_ia)
repo = st.secrets["DISPLAY_NAME"]
print("Repo display name: " + repo)


# Inicializamos objeto para gestionar las interacciones con el agente de IA. No creamos el storage sino que lo recuperamos
ia_agent = InvestigationAgent(display_name=repo, instructions=instructions_ia, ia_model=modelo_ia, create_store=False)



###################################################################
# Código visual Streamlit
###################################################################

st.title("Chatbot para analizar programas de ayuda a la investigación")
st.logo("resources/fiibhuilhuse.png", size="54px")

# Botón para resetear
st.button('Vaciar Chat', on_click=reset_conversation)

# Botón para subir un ficheros y anexarlo al chat
#str_document = None     #inicializamos vacío
uploaded_file = st.file_uploader("Adjuntar fichero al chat")
# escribimos a disco el fichero
if uploaded_file: # check if path is not None
    with open("docs/" + uploaded_file.name, mode='wb') as w:
        w.write(uploaded_file.getvalue())
    loader = PyPDFLoader("docs/" + uploaded_file.name)
    pages = loader.load_and_split()
    str_document = "Documento adjunto:\n"
    os.remove("docs/" + uploaded_file.name)
    for page in pages:
        str_document += page.page_content + "\n"   #cada página la separamos con un retorno de línea
    st.session_state.embedded_doc = str_document
    print("Adjuntado el documento " + "docs/" + uploaded_file.name)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("En que puedo ayudarte?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


# Display assistant response in chat message container
with st.chat_message("assistant"):
    response = "En qué te puedo ayudar?"
    if len(st.session_state.messages) > 0:
        message_str = get_txt_messages(st.session_state.messages)
        print("Query para la IA:")
        print(message_str)
        query_ia = message_str
        if uploaded_file:   #si hay documento adjunto, se anexa al principio de la pregunta
            query_ia = str_document + query_ia
        response = ia_agent.chat(query_ia)
        st.write(response)
    else:
        st.write(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
