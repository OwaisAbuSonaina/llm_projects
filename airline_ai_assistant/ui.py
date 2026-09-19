import os

import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="FlightAI", page_icon="✈️", layout="wide")
st.title("FlightAI Assistant")
st.caption("Ask for flights to your preferred destination.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Where would you like to fly?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat",
            json={"message": prompt},
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
        bot_message = payload["summary"]
    except requests.RequestException as exc:
        bot_message = f"Sorry, I couldn't reach the FlightAI API. Error: {exc}"

    st.session_state.messages.append({"role": "assistant", "content": bot_message})
    with st.chat_message("assistant"):
        st.markdown(bot_message)
