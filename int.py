import os
import time
from datetime import datetime
from tkinter import Tk, messagebox
from file import load_database, save_database, calculate_file_hash, backup_file, generate_report

# Show a notification for file changes
def show_notification(filepath, change_type, severity="Unknown"):
    root = Tk()
    root.withdraw()
    messagebox.showinfo(
        "File Integrity Alert",
        f"File: {filepath}\nChange: {change_type}\nSeverity: {severity}"
    )
    root.destroy()

# Add a new file to the database
def add_new_file(filepath, database):
    file_hash = calculate_file_hash(filepath)
    if file_hash:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        database[filepath] = [{"hash": file_hash, "timestamp": timestamp}]
        backup_file(filepath, timestamp)
        print(f"New file added: {filepath}")
        show_notification(filepath, "New file added", "Low Risk")

# Check integrity of files and directories
def check_file_integrity(database):
    monitored_paths = list(database.keys())
    current_files = set()

    for path in monitored_paths:
        if os.path.isfile(path):
            # Handle individual files
            current_hash = calculate_file_hash(path)
            last_hash = database[path][-1]["hash"]

            if current_hash is None:
                # File deleted
                print(f"File deleted: {path}")
                show_notification(path, "Deleted", "Critical")
                del database[path]
            elif current_hash != last_hash:
                # File modified
                severity = generate_report(path, last_hash, current_hash)
                print(f"Change detected in {path}. Severity: {severity}")
                show_notification(path, "Modified", severity)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                backup_file(path, timestamp)
                database[path].append({"hash": current_hash, "timestamp": timestamp})

        elif os.path.isdir(path):
            # Handle directories: Traverse and check files
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    current_files.add(file_path)

                    if file_path not in database:
                        # New file detected
                        add_new_file(file_path, database)
                    else:
                        # Check existing file for modifications
                        current_hash = calculate_file_hash(file_path)
                        last_hash = database[file_path][-1]["hash"]
                        if current_hash != last_hash:
                            severity = generate_report(file_path, last_hash, current_hash)
                            print(f"Change detected in {file_path}. Severity: {severity}")
                            show_notification(file_path, "Modified", severity)
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            backup_file(file_path, timestamp)
                            database[file_path].append({"hash": current_hash, "timestamp": timestamp})

    # Detect deleted files
    for file_path in monitored_paths:
        if not os.path.exists(file_path):
            print(f"File deleted: {file_path}")
            show_notification(file_path, "Deleted", "Critical")
            del database[file_path]

def main():
    database = load_database()
    if not database:
        print("No files or directories to monitor.")
        return

    try:
        while True:
            print("Monitoring files and directories...")
            check_file_integrity(database)
            save_database(database)
            time.sleep(10)  # Monitor every 10 seconds
    except KeyboardInterrupt:
        print("Monitoring stopped.")

if __name__ == "__main__":
    main()
