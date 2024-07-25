import streamlit as st
from chat_data import save_message, get_messages

def main():
    st.subheader("Forum")

    # User input for message
    user = st.text_input("NickName", key="user_input", placeholder="Enter your nickname")
    message = st.text_input("Message", key="message_input", placeholder="Type your views here...")

    # Submit message
    if st.button("Send"):
        if user and message:
            save_message(user, message)
            st.success("Message sent!")
        else:
            st.error("Please enter both a nickname and a message.")

    # Display chat messages
    st.write("### Chat History")

    messages = get_messages()
    if messages:
        for msg in messages:
            st.markdown(
                f"<div style='padding: 10px; border-bottom: 1px solid #ddd;'>"
                f"<strong style='color: #007BFF;'>{msg[0]}</strong> <span style='color: #888;'>{msg[2]}</span><br>"
                f"<p>{msg[1]}</p>"
                f"</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("No messages yet. Start the conversation!")

if __name__ == "__main__":
    main()
