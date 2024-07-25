import streamlit as st
import pickle
import bcrypt
from pathlib import Path

# Load passwords from a pickle file
def load_passwords():
    file_path = Path(__file__).parent / "hashed_pw.pkl"
    if file_path.exists():
        with file_path.open("rb") as file:
            names, usernames, hashed_passwords = pickle.load(file)
    else:
        names, usernames, hashed_passwords = [], [], []
    return names, usernames, hashed_passwords

# Save passwords to a pickle file
def save_passwords(names, usernames, hashed_passwords):
    file_path = Path(__file__).parent / "hashed_pw.pkl"
    with file_path.open("wb") as file:
        pickle.dump((names, usernames, hashed_passwords), file)

def main():
    st.markdown("<h1 style='text-align: center;'>📈 SMART FORESIGHT Login/Signup</h1>", unsafe_allow_html=True)
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.experimental_rerun()

    # Load existing credentials
    names, usernames, hashed_passwords = load_passwords()

    # Add a tab to switch between login and signup
    login_signup = st.selectbox("Choose an option", ["Login", "Signup"])

    if login_signup == "Login":
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

    elif login_signup == "Signup":
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        signup_button = st.button("Signup")

        if signup_button:
            if new_username in usernames:
                st.error("Username already exists")
            else:
                hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                names.append(new_username)  # Optionally store real names
                usernames.append(new_username)
                hashed_passwords.append(hashed_pw.decode('utf-8'))
                save_passwords(names, usernames, hashed_passwords)
                st.success("Signup successful! You can now log in.")
                

if __name__ == "__main__":
    main()
