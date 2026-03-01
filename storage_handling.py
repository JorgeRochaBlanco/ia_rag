from dotenv import load_dotenv
import os
from pathlib import Path
import streamlit as st

from app.agent_investigacion import InvestigationAgent


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
tmp_ruta = "docs"


# Controles Streamlit

st.title("Limpieza y recarga de documentos al repositorio - " + repo)

# Initialize client (requires GEMINI_API_KEY environment variable), creating new storage
ia_agent = InvestigationAgent(display_name=repo, instructions=instructions_ia, ia_model=modelo_ia, create_store=True)
st.write("Repositorio limpio y recreado")

# Subimos ficheros al repo
uploaded_files = st.file_uploader(
    label="Subir ficheros",
    type=['pdf'],
    accept_multiple_files=True,
    key="fileUploader",
    help="Seleccione uno o varios ficheros"
)
for file in uploaded_files:
    # Sube el fichero al repositorio de IA
    st.write("Fichero:", file.name)
    #grabamos en disco
    bytes_data = file.read()  # read the content of the file in binary
    print(file.name, bytes_data)
    with open(os.path.join(tmp_ruta, file.name), "wb") as f:
        f.write(bytes_data)  # write this content elsewhere

#functions.upload_documents(client, store.name, Path(tmp_ruta))  #subimos los ficheros al repo
ia_agent.upload_documents(Path(tmp_ruta))
# List all files in the directory
for filename in os.listdir(tmp_ruta):
    file_path = os.path.join(tmp_ruta, filename)
    
    # Check if it is a file (not a subdirectory)
    if os.path.isfile(file_path):
        os.remove(file_path)  # Remove the file
        print(f"Deleted file: {filename}")
