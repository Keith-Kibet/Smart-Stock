import streamlit as st
import pickle
import bcrypt
from pathlib import Path

# Load passwords from a pickle file
def load_passwords():
    file_path = Path(__file__).parent / "hashed_pw.pkl"
    with file_path.open("rb") as file:
        names, usernames, hashed_passwords = pickle.load(file)
    return names, usernames, hashed_passwords

# Main function for the login page
def main():
    st.set_page_config(page_title="Login", layout="wide")
    st.markdown("<h1 style='text-align: center;'>📈 Stock Data Login</h1>", unsafe_allow_html=True)
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.experimental_rerun()

    names, usernames, hashed_passwords = load_passwords()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username in usernames:
            index = usernames.index(username)
            if bcrypt.checkpw(password.encode('utf-8'), hashed_passwords[index].encode('utf-8')):
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("Incorrect password")
        else:
            st.error("Username not found")

if __name__ == "__main__":
    main()
