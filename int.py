import hashlib
import json
import os
import time
from datetime import datetime
from tkinter import Tk, messagebox

# Define the database file path
DATABASE_FILE = "hash_database.json"

# Load existing database or create a new one
def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    return {}

# Calculate the hash of a file
def calculate_file_hash(filepath):
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None

# Show a pop-up notification for a modified file
def show_notification(filepath):
    # Create a single Tkinter window for the notification
    root = Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("File Integrity Alert", f"File modified: {filepath}")
    root.destroy()  # Close the Tkinter instance after the message is displayed

# Check the integrity of files in the database and show notifications on change
def check_file_integrity(database):
    for filepath, entries in database.items():
        last_saved_hash = entries[-1]["hash"]  # Get the last saved hash
        current_hash = calculate_file_hash(filepath)
        
        if current_hash is None:
            continue  # Skip if the file is not found

        # Check if the hash has changed and show a notification for each modified file
        if current_hash != last_saved_hash:
            print(f"Change detected in {filepath}. Showing notification.")
            show_notification(filepath)  # Show a notification for the modified file
            time.sleep(60)  # Wait 1 minute before checking again
            current_hash = calculate_file_hash(filepath)  # Recalculate hash

        # Update the hash in the database if it has changed
        if current_hash != entries[-1]["hash"]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_entry = {"hash": current_hash, "timestamp": timestamp}
            database[filepath].append(new_entry)
            print(f"Updated hash for {filepath} in database.")

def save_database(database):
    with open(DATABASE_FILE, "w") as f:
        json.dump(database, f, indent=4)

def main():
    database = load_database()
    if not database:
        print("No files to monitor.")
        return

    try:
        while True:
            print("Monitoring files...")  # Message to show monitoring is active
            check_file_integrity(database)
            save_database(database)
            time.sleep(30)  # Wait for 30 seconds before the next check
    except KeyboardInterrupt:
        print("Monitoring stopped.")

if __name__ == "__main__":
    main()
