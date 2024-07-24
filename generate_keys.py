import pickle
from pathlib import Path
import bcrypt

names = ["Esther Kadzo", "Silvestus Fadhili", "Amira Fadhili"]
usernames = ["EssyK", "SFadhili", "Amira"]
passwords = ["abc123", "sf345", "af678"]

# Hash the passwords using bcrypt
hashed_passwords = [bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') for password in passwords]

# Save the names, usernames, and hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump((names, usernames, hashed_passwords), file)
