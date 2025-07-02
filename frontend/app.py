import streamlit as st
import requests

st.title("🗓️ Calendar Booking Assistant")
chat_history = st.session_state.get("history", [])

user_input = st.text_input("You:", key="user_input")

if user_input:
    response = requests.post("https://calendar-booking-agent-2mnt.onrender.com/chat", json={"message": user_input})
    res_json = response.json()
    print(res_json)  # for debugging, remove later
    if "response" in res_json and isinstance(res_json["response"], dict) and "response" in res_json["response"]:
        bot_reply = res_json["response"]["response"]
    else:
        bot_reply = "Sorry, something went wrong!"
    chat_history.append(("You", user_input))
    chat_history.append(("Bot", bot_reply))
    st.session_state["history"] = chat_history

for speaker, msg in chat_history:
    st.markdown(f"**{speaker}:** {msg}")