import os
from pathlib import Path
from google import genai


#####################################################################
# Funciones para manejar repositorios y búsquedas

def create_store(client: genai.Client, display_name: str) -> genai.types.FileSearchStore:
    """Create a file search store for organizing searchable documents."""
    store = client.file_search_stores.create(config={"display_name": display_name})
    print(f"Almacenamiento creado: {store.name}")
    return store


def upload_documents(client: genai.Client, store_name: str, docs_path: Path) -> None:
    """Upload all PDF documents from the specified directory to the store."""
    print("\nCargando documentos...")
    for file_path in docs_path.glob("*.pdf"):
        file = client.file_search_stores.upload_to_file_search_store(
            file=file_path,
            file_search_store_name=store_name,
            config={"display_name": file_path.name},
        )
        print(f"Documento cargado: {file.name}")


def upload_document(client: genai.Client, store_name: str, file_name, ruta: str) -> None:
    """Upload all PDF documents from the specified directory to the store."""
    print("\nCargando documentos...")
    file = client.file_search_stores.upload_to_file_search_store(
        file=file_name,
        file_search_store_name=store_name,
        config={"display_name": file_name},
    )
    print(f"Documento cargado: {file.name}")


def get_store(client: genai.Client, store_name: str):
    result = None
    for store in client.file_search_stores.list():
        if store_name == store.display_name:
            result = store
    return result


def list_documents(client: genai.Client, store_name: str = None) -> str:
    print("\nListamos documentos y los storages...")
    file_search_store = None
    l_desc = []
    for store in client.file_search_stores.list():
        if store.display_name == store_name or store_name == None:
            file_search_store = store
            store_count = file_search_store.active_documents_count
            print(f"Found existing store at {file_search_store.name}")
            print(f"Total docs: {store_count}")
            l_desc.append(store.display_name + " - " + str(store_count))
    return ", ".join(l_desc)


def search(client: genai.Client, store_name: str, instructions: str, query: str) -> str:
    """Query the store using Gemini with file search."""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=instructions + "\n" + query,  #instrucciones generales y la lista de preguntas y respuestas previas
        config={"tools": [{"file_search": {"file_search_store_names": [store_name]}}]},
    )
    return response.text


def search_stream(client: genai.Client, store_name: str, instructions: str, query: str) -> str:
    """Query the store using Gemini with file search."""
    response_generator = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=instructions + "\n" + query,  #instrucciones generales y la lista de preguntas y respuestas previas,
        config={"tools": [{"file_search": {"file_search_store_names": [store_name]}}]}
    )
    return response_generator


def cleanup(client: genai.Client) -> None:
    """Delete all file search stores (force deletes documents and chunks too)."""
    print("\nEliminando recursos previos...")
    for store in client.file_search_stores.list():
        client.file_search_stores.delete(name=store.name, config={"force": True})
        print(f"Almacenamiento eliminado: {store.name}")
    print("Limpieza terminada.")
