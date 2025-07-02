import streamlit as st
import requests

st.title("🗓️ Calendar Booking Assistant")
chat_history = st.session_state.get("history", [])

user_input = st.text_input("You:", key="user_input")

if user_input:
    response = requests.post("https://calendar-booking-agent-2mnt.onrender.com", json={"message": user_input})
    bot_reply = response.json()["response"]["response"]
    chat_history.append(("You", user_input))
    chat_history.append(("Bot", bot_reply))
    st.session_state["history"] = chat_history

for speaker, msg in chat_history:
    st.markdown(f"**{speaker}:** {msg}")