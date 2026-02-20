#import chainlit as cl
import streamlit as st

from dotenv import load_dotenv
from app.agent import FAQAgent

# Load environment variables
load_dotenv()

# Initializa agent
agent = FAQAgent()


import streamlit as st
import random
import time

st.title("Chat con IA para programas de investigación")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("En qué te puedo ayudar?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Display assistant response in chat message container
with st.chat_message("assistant"):
    response = agent.chat(st.session_state.messages["content"])
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})




# Get response from agent
#response = agent.chat(message.content)
