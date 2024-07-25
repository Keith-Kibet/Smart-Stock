# chat_data.py
import csv
from datetime import datetime

CSV_FILE = 'chat_messages.csv'

# Ensure the CSV file exists and has the correct headers
def initialize_csv():
    try:
        with open(CSV_FILE, 'r', newline='') as file:
            pass
    except FileNotFoundError:
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['User', 'Message', 'Timestamp'])

# Save a new message to the CSV file
def save_message(user, message):
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user, message, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

# Get all messages from the CSV file
def get_messages():
    messages = []
    with open(CSV_FILE, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        messages = list(reader)
    return messages

# Initialize CSV on script load
initialize_csv()
