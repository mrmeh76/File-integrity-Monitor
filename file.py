import hashlib
import json
import os
from datetime import datetime

# Define the database file path
DATABASE_FILE = "hash_database.json"

# Load existing database or create a new one
def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    return {}

# Save database
def save_database(database):
    with open(DATABASE_FILE, "w") as f:
        json.dump(database, f, indent=4)

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

# Add a file to the database
def add_file(filepath, database):
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return

    file_hash = calculate_file_hash(filepath)
    if file_hash is None:
        return

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"File {filepath} is being added to the database.")

    new_entry = {
        "hash": file_hash,
        "timestamp": current_time
    }

    database[filepath] = [new_entry]
    print(f"Added {filepath} with new hash and timestamp.")

# Save current hash for any monitored file
def save_current_hash(database):
    if not database:
        print("No files in the database to save.")
        return

    print("\nFiles in database:")
    files = list(database.keys())
    for i, filepath in enumerate(files, 1):
        print(f"{i}. {filepath}")

    try:
        choice = int(input("Enter the number of the file to save the current hash: "))
        filepath = files[choice - 1]

        # Calculate and save the current hash
        file_hash = calculate_file_hash(filepath)
        if file_hash is None:
            return

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {
            "hash": file_hash,
            "timestamp": current_time
        }
        database[filepath].append(new_entry)
        print(f"Current hash saved for {filepath}.")
    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid number.")

# Remove a file from the database with a selection menu
def remove_file(database):
    if not database:
        print("No files in the database to remove.")
        return

    print("\nFiles in database:")
    files = list(database.keys())
    for i, filepath in enumerate(files, 1):
        print(f"{i}. {filepath}")

    try:
        choice = int(input("Enter the number of the file to remove: "))
        filepath = files[choice - 1]
        del database[filepath]
        print(f"Removed {filepath} from database.")
    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid number.")

def main():
    database = load_database()

    while True:
        print("\nFile Integrity Manager")
        print("1. Add file")
        print("2. Save current hash of a monitored file")
        print("3. Remove file")
        print("4. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            filepath = input("Enter the file path to add: ")
            add_file(filepath, database)
        elif choice == "2":
            save_current_hash(database)
        elif choice == "3":
            remove_file(database)
        elif choice == "4":
            save_database(database)
            print("Database saved. Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

