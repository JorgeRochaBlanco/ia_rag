import os
from pathlib import Path
from google import genai
from google.genai import types


class InvestigationAgent:
    """Minimal agent using Gemini's File Search tool."""

    def __init__(self, display_name: str, instructions: str, ia_model: str, create_store = False):
        """Constructor. Neceista el display name del storage, las instrucciones de entramiento e identificar el modelo IA a usar"""
        self.client = genai.Client()
        self.ia_model = ia_model
        self.display_name = display_name
        if create_store:   #con esta variable se decide si se recrea el storage (incializador) o se recupera (chat)
            self.store = self.create_store(self.display_name)
        else:
            self.store = self.get_store()
        self.instructions = instructions or ""

        if not self.store.name:
            raise ValueError("Store name required (or set STORE_NAME env var)")

    def chat(self, query: str) -> str:
        """Query the store using Gemini with file search. No appending is done for Q&A, has to be done outside if necessary"""
        response = self.client.models.generate_content(
            model=self.ia_model,
            contents=self.instructions + "\n" + query,  #instrucciones generales y la lista de preguntas y respuestas previas
            config={"tools": [{"file_search": {"file_search_store_names": [self.store.name]}}]},
        )
        return response.text


    ## Métodos auxiliares para gestionar repositorios, cargar datos de configuración, etc.
    def create_store(self, display_name_storage: str) -> genai.types.FileSearchStore:
        """Create a file search store for organizing searchable documents."""
        store = self.client.file_search_stores.create(config={"display_name": display_name_storage})
        print(f"Almacenamiento creado: {store.name}")
        return store

    def get_store(self):
        result = None
        for store in self.client.file_search_stores.list():
            if self.display_name == store.display_name:
                result = store
        return result
    
    def cleanup(self) -> None:
        """Delete all file search stores (force deletes documents and chunks too)."""
        print("\nEliminando recursos previos...")
        for store in self.client.file_search_stores.list():
            self.client.file_search_stores.delete(name=store.name, config={"force": True})
            print(f"Almacenamiento eliminado: {store.name}")
        print("Limpieza terminada.")

    def upload_documents(self, docs_path: Path) -> None:
        """Upload all PDF documents from the specified directory to the store."""
        print("\nCargando documentos...")
        for file_path in docs_path.glob("*.pdf"):
            file = self.client.file_search_stores.upload_to_file_search_store(
                file=file_path,
                file_search_store_name=self.store.name,
                config={"display_name": file_path.name},
            )
            print(f"Documento cargado: {file.name}")


    def list_documents(self) -> str:
        print("\nListamos documentos y los storages...")
        file_search_store = None
        l_desc = []
        for store in self.client.file_search_stores.list():
            if store.display_name == self.display_name or self.display_name == None:
                file_search_store = store
                store_count = file_search_store.active_documents_count
                print(f"Found existing store at {file_search_store.name}")
                print(f"Total docs: {store_count}")
                l_desc.append(store.display_name + " - " + str(store_count))
        return ", ".join(l_desc)


    @staticmethod
    def load_instructions(instr_file: str) -> str:
        """Cargamos instrucciones de un fichero. En caso de error no se devuelve nada"""
        contenido = ''   #por defecto no se devuelven instrucciones
        try:
            with open('config/'+instr_file, 'r', encoding='utf-8') as file:
                contenido = file.read()
            print("Instrucciones cargadas con éxito.")
            # print(contenido) # Para ver el contenido
        except FileNotFoundError:
            print("El archivo no existe.")
        return contenido
