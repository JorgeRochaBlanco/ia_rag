from dotenv import load_dotenv
import os
from pathlib import Path
from google import genai
import streamlit as st

from app import functions


# Load environment variables
load_dotenv()

SYSTEM_PROMPT = """
Eres un agente para apoyar al personal de gestión de las investigaciones. 
Solo estás preparado para responder preguntas que provengan de tu base de conocimientos.
Si la respuesta no está en esa base de conocimientos, responde:

Lo lamento, pero solo puedo contestar preguntas que estén en mi base de conocimiento.

<reglas>
- Devuelve respuestas directas (2 - 3 frases si es posible)
- Usa bullets si la lista de respuestas es de 3+ elementos
- Incluye fechas o cifras específicas cuando sea relevante
- Sé correcto y amigable
</reglas>
"""

repo = "BD Investigacion"

print("Nombre de Storage Google: ", end="\t")
print(os.getenv("STORE_NAME"))
print("API Key: ", end="\t")
print(os.getenv("GEMINI_API_KEY"))


# Funciones auiliares
def get_txt_messages(messages):
    return "".join([item["role"]+": "+(item["content"] if item["content"] else "")+"\n" for item in messages])


# Initialize client (requires GEMINI_API_KEY environment variable)
client = genai.Client()
# Recuperamos el storage
store = None
# for store_item in client.file_search_stores.list():
#     disp_name = store_item.display_name
#     name = store_item.name
#     count_docs = store_item.active_documents_count
#     print(f"Recuperado storage, display name {disp_name}, nombre {name} y {count_docs} documentos")
store = functions.get_store(client=client, store_name=repo)  #por defecto tenemos un Store
print(f"Recuperado storage, display name {store.display_name}, nombre {store.name} y {store.active_documents_count} documentos")



###################################################################
# Código Streamlit
###################################################################

st.title("Chat aumentado por RAG")

# Función para resetear el chat
def reset_conversation():
  st.session_state.conversation = None
  st.session_state.chat_history = None

# Botón para resetear
st.button('Vaciar Chat', on_click=reset_conversation)


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
        response = functions.search(client=client, store_name=store.name, instructions=SYSTEM_PROMPT, query=message_str)
        st.write(response)
    else:
        st.write(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})