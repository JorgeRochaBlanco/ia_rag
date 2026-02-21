import os
from google import genai
from google.genai import types

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


class InvestigationAgent:
    """Minimal agent using Gemini's File Search tool."""

    def __init__(self, store_name: str | None = None):
        self.client = genai.Client()
        self.store_name = store_name or os.getenv("STORE_NAME")

        if not self.store_name:
            raise ValueError("Store name required (or set STORE_NAME env var)")

    def chat(self, message: str) -> str:
        """Query the store using Gemini with file search."""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message,
            config={"tools": [{"file_search": {"file_search_store_names": [self.store_name]}}]},
        )
        return response.text
