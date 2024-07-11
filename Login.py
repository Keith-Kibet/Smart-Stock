import streamlit as st
import sqlite3
from datetime import datetime, timedelta
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import secrets
from flask import Flask, request, jsonify
from flask_mail import Mail, Message

# Initialize Streamlit app
st.title("Login / Sign-Up Page")

# Initialize Flask app for email confirmation
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MAIL_SERVER'] = 'smtp.yourmailserver.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password_here'

mail = Mail(app)

# Database initialization
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL UNIQUE,
              email TEXT NOT NULL UNIQUE,
              password TEXT NOT NULL,
              confirmed INTEGER DEFAULT 0,
              confirmation_token TEXT,
              registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
          ''')
conn.commit()

ph = PasswordHasher()

# Streamlit pages
page = st.sidebar.radio("Menu", ['Login', 'Sign Up'])

if page == 'Sign Up':
    st.subheader('Create an Account')
    username = st.text_input('Username')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')

    if st.button('Sign Up'):
        if password == confirm_password:
            hashed_password = ph.hash(password)
            confirmation_token = secrets.token_hex(16)
            c.execute('INSERT INTO users (username, email, password, confirmation_token) VALUES (?, ?, ?, ?)',
                      (username, email, hashed_password, confirmation_token))
            conn.commit()

            # Send confirmation email
            confirm_url = f"http://localhost:5000/confirm/{confirmation_token}"
            msg = Message('Confirm Your Email', sender='your_email@example.com', recipients=[email])
            msg.body = f'Click this link to confirm your email: {confirm_url}'
            mail.send(msg)

            st.success('You have successfully registered! Please check your email to confirm.')

        else:
            st.error('Passwords do not match.')

elif page == 'Login':
    st.subheader('Log In')
    login_email = st.text_input('Email')
    login_password = st.text_input('Password', type='password')

    if st.button('Log In'):
        c.execute('SELECT * FROM users WHERE email=?', (login_email,))
        user = c.fetchone()

        if user:
            try:
                if ph.verify(user[3], login_password):
                    if user[4] == 1:  # Check if email is confirmed
                        st.success(f'Logged in as {user[1]}')
                    else:
                        st.error('Please confirm your email to log in.')
                else:
                    st.error('Incorrect password.')
            except VerifyMismatchError:
                st.error('Incorrect password.')
        else:
            st.error('Email not registered.')

# Flask routes for email confirmation
@app.route('/confirm/<token>')
def confirm_email(token):
    c.execute('SELECT * FROM users WHERE confirmation_token=?', (token,))
    user = c.fetchone()
    if user:
        c.execute('UPDATE users SET confirmed=1, confirmation_token=NULL WHERE id=?', (user[0],))
        conn.commit()
        return 'Email confirmed successfully. You can now log in.'
    else:
        return 'Invalid confirmation link.'

# Run the app without debug mode in Streamlit environment
# if __name__ == '__main__':
#    app.run(debug=True)

