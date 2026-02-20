#import chainlit as cl
import streamlit as st

from dotenv import load_dotenv
from app.agent import FAQAgent

# Load environment variables
load_dotenv()

# Initializa agent
agent = FAQAgent()

# Title
st.title("ChatGPT-like clone")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message):
        st.markdown(message)

# Accept user input
if prompt := st.chat_input("Qué quieres saber?"):
    # Add user message to chat history
    st.session_state.messages.append(prompt)
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

# Display assistant response in chat message container
with st.chat_message("assistant"):
    # Get response from agent
    response = agent.chat(message.content)

st.session_state.messages.append(response)
