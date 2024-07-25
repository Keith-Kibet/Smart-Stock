# chat.py
import streamlit as st
from chat_data import save_message, get_messages

def main():
    st.subheader("Chat")

    # User input for message
    user = st.text_input("NickName", key="user_input")
    message = st.text_input("Message", key="message_input")

    # Submit message
    if st.button("Send"):
        if user and message:
            save_message(user, message)
            st.success("Message sent!")
        else:
            st.error("Please enter both user name and message.")

    # Display chat messages
    st.write("### Chat History")
    messages = get_messages()
    for msg in messages:
        st.write(f"[{msg[2]}] **{msg[0]}**: {msg[1]}")
