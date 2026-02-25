from dotenv import load_dotenv
import os
from pathlib import Path
import streamlit as st

from app.agent_investigacion import InvestigationAgent


# Load environment variables
load_dotenv()

#instrucciones para la IA, por si hay varias disponibles
instructions_ia = InvestigationAgent.load_instructions(os.getenv("FICH_INSTRUCCIONES_IA"))
#tomamos variables de entorno para configurar accesos a Storage e instrucciones para agente IA
print("Modelo IA a usar:", end="\t")
modelo_ia = os.getenv("IA_MODEL")
print(modelo_ia)
print("Nombre de Storage Google: ", end="\t")
print(os.getenv("STORE_NAME"))
print("API Key: ", end="\t")
print(os.getenv("GEMINI_API_KEY"))
print("Instrucciones para el agente:")
print(instructions_ia)
repo = os.getenv("DISPLAY_NAME")
print("Repo display name: " + repo)
tmp_ruta = "docs"


# Controles Streamlit

st.title("Limpieza y recarga de documentos al repositorio - " + repo)

# Initialize client (requires GEMINI_API_KEY environment variable), creating new storage
ia_agent = InvestigationAgent(display_name=repo, instructions=instructions_ia, ia_model=modelo_ia, create_store=True)

#functions.cleanup(client)
#store = functions.create_store(client, repo)
#print("Store:")
#print(store)

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


# # Step 3: Query the documents
# search(client, store.name, "Cuántas ayudas distintas para investigación tienes registradas en tu base de conocimiento? Cuéntalas y haz un listado de las mismas")

# # Step 4: Clean up all stores
# # cleanup(client)
