import hashlib
import json
import os
from datetime import datetime
import shutil

# Define constants
DATABASE_FILE = "hash_database.json"
BACKUP_DIR = "backup_files"

# Load or initialize the database
def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    return {}

# Save the database
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

# Backup a file with a timestamp
def backup_file(filepath, timestamp):
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    filename = os.path.basename(filepath)
    backup_path = os.path.join(BACKUP_DIR, f"{filename}_{timestamp.replace(':', '-')}.bak")
    shutil.copy(filepath, backup_path)
    print(f"Backup created for {filepath} at {backup_path}")

# Restore a file from backup
def restore_file(filepath, timestamp):
    filename = os.path.basename(filepath)
    backup_path = os.path.join(BACKUP_DIR, f"{filename}_{timestamp.replace(':', '-')}.bak")
    if os.path.exists(backup_path):
        shutil.copy(backup_path, filepath)
        print(f"File {filepath} restored to version from {timestamp}.")
    else:
        print(f"Backup for {timestamp} not found.")

# Add a file to the database
def add_file(filepath, database):
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return

    file_hash = calculate_file_hash(filepath)
    if file_hash is None:
        return

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    database[filepath] = [{"hash": file_hash, "timestamp": current_time}]
    backup_file(filepath, current_time)
    print(f"Added {filepath} to monitoring with a backup created.")

# Add all files in a directory to the database
def add_directory(directory, database):
    if not os.path.exists(directory) or not os.path.isdir(directory):
        print(f"Directory {directory} does not exist.")
        return

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            add_file(file_path, database)

    print(f"Added all files in directory {directory} to monitoring.")

# Remove a file or directory from the database
def remove_entry(database):
    if not database:
        print("No files or directories in the database.")
        return

    print("\nMonitored entries:")
    files = list(database.keys())
    for i, path in enumerate(files, 1):
        print(f"{i}. {path}")

    try:
        choice = int(input("Enter the number of the file or directory to remove: "))
        path = files[choice - 1]
        del database[path]
        print(f"Removed {path} from monitoring.")
    except (ValueError, IndexError):
        print("Invalid selection.")

# Generate a report based on file changes (hash comparison and size difference)
def generate_report(filepath, old_hash, new_hash):
    try:
        old_size = os.path.getsize(filepath)
        new_size = os.path.getsize(filepath)
        size_difference = abs(new_size - old_size)
        percent_difference = (size_difference / old_size) * 100 if old_size > 0 else 100

        if percent_difference > 50:
            severity = "Critical"
        elif percent_difference > 20:
            severity = "Moderate"
        else:
            severity = "Low Risk"

        print(f"Report for {filepath}:")
        print(f"  - Old Hash: {old_hash}")
        print(f"  - New Hash: {new_hash}")
        print(f"  - Size Change: {size_difference} bytes ({percent_difference:.2f}%)")
        print(f"  - Severity: {severity}")
        return severity

    except Exception as e:
        print(f"Error generating report for {filepath}: {e}")
        return "Unknown"

def main():
    database = load_database()

    while True:
        print("\nFile Integrity Manager")
        print("1. Add file or directory")
        print("2. Remove file or directory")
        print("3. Restore a file from backup")
        print("4. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            path = input("Enter the file or directory path to add: ")
            if os.path.isfile(path):
                add_file(path, database)
            elif os.path.isdir(path):
                add_directory(path, database)
            else:
                print("Invalid path. Please enter a valid file or directory.")
        elif choice == "2":
            remove_entry(database)
        elif choice == "3":
            filepath = input("Enter the file path to restore: ")
            timestamp = input("Enter the timestamp of the backup to restore (YYYY-MM-DD HH:MM:SS): ")
            restore_file(filepath, timestamp)
        elif choice == "4":
            save_database(database)
            print("Database saved. Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
