import chainlit as cl

from dotenv import load_dotenv
from app.agent import FAQAgent

# Load environment variables
load_dotenv()


@cl.on_chat_start
async def start():
    """Initialize the agent when a new chat session starts."""
    try:
        agent = FAQAgent()
        cl.user_session.set("agent", agent)

        await cl.Message(
            content="Hola, soy el agente para analizar convocatorias de investigación. ¿Cómo puedo ayudarte?"
        ).send()
    except ValueError as e:
        await cl.Message(
            content=f"⚠️ Error de configuración: {e}\n\nPor favor, especifica el nombre del Storage de Google"
        ).send()


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages."""
    agent = cl.user_session.get("agent")

    if not agent:
        await cl.Message(
            content="Agente no inicializado. Por favor, refresca la página."
        ).send()
        return

    # Get response from agent
    response = agent.chat(message.content)

    # Create citation elements if we have any
    elements = []
    if response.citations:
        # Add citations as text elements
        for i, citation in enumerate(response.citations, 1):
            elements.append(
                cl.Text(name=f"Source {i}", content=citation, display="side")
            )

    # Send response with citations
    await cl.Message(content=response.text, elements=elements).send()
