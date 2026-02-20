"""The world's most minimal AI RAG agent ever"""

import os
from google import genai
from google.genai import types

SYSTEM_PROMPT = """
You are a helpful assistant.

Only answer questions that come from your knowledge base.

If the answer is not in your knowledge base, say:

Sorry, I don't know the answer to that question. If you need 
further help, please contact our support team.
"""


class SimpleAgent:
    """Minimal agent using Gemini's File Search tool."""

    def __init__(self, store_name: str | None = None):
        self.client = genai.Client()
        self.store_name = store_name or os.getenv("STORE_NAME")

        if not self.store_name:
            raise ValueError("Store name required (or set STORE_NAME env var)")

    def chat(self, message: str) -> str:
        """Send a message and get a response."""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[self.store_name]
                        )
                    )
                ],
            ),
        )
        return response.text
