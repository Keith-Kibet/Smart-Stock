import pickle
from pathlib import Path

def load_passwords():
    file_path = Path(__file__).parent / "hashed_pw.pkl"
    with file_path.open("rb") as file:
        data = pickle.load(file)
    print(data)  # Inspect the content
    return data

load_passwords()
