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


prompt = st.chat_input("En qué te puedo ayudar?")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
    response = agent.chat(prompt)
    st.write(response)