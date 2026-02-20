"""
Gemini File Search API Demo

Demonstrates the core workflow:
1. Create a file search store
2. Upload and index documents
3. Query documents using Gemini
4. Clean up resources
"""

from pathlib import Path
from google import genai
import os
from dotenv import load_dotenv

# Cargamos variables de entorno desde el archivo .env
load_dotenv()

def create_store(
    client: genai.Client, display_name: str
) -> genai.types.FileSearchStore:
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


def search(client: genai.Client, store_name: str, query: str) -> str:
    """Query the store using Gemini with file search."""
    print(f"\nPreguntando en la base de conocimientos: '{query}'...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config={"tools": [{"file_search": {"file_search_store_names": [store_name]}}]},
    )
    print(f"\nAnswer:\n{response.text}")
    return response.text


def cleanup(client: genai.Client) -> None:
    """Delete all file search stores (force deletes documents and chunks too)."""
    print("\nEliminando recursos previos...")
    for store in client.file_search_stores.list():
        client.file_search_stores.delete(name=store.name, config={"force": True})
        print(f"Almacenamiento eliminado: {store.name}")
    print("Limpieza terminada.")


if __name__ == "__main__":
    # Initialize client (requires GEMINI_API_KEY environment variable)
    client = genai.Client()

    # Step 1: Create a file search store. First, clean up any existing stores to avoid clutter (optional).
    cleanup(client)
    store = create_store(client, "FAQ Store")

    # Step 2: Upload documents
    upload_documents(client, store.name, Path("docs_investigacion"))

    # Step 3: Query the documents
    search(client, store.name, "Cuántas ayudas distintas para investigación tienes registradas en tu base de conocimiento? Cuéntalas y haz un listado de las mismas")

    # Step 4: Clean up all stores
    # cleanup(client)
