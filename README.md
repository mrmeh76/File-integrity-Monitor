<h1 align="center">File Integrity Checker Tool</h1>

## Description

The **File Integrity Checker Tool** is a **Python-based** utility that helps in monitoring and ensuring the integrity of files by checking their hash values. It calculates the hash of monitored files and stores them in a local JSON database. When a file is modified, the tool compares the file’s current hash with the previously stored hash and sends a pop-up notification if any modification is detected.

This tool can be used to track changes in files, especially for use cases where file integrity is critical (e.g., configuration files, logs, or code files). It also provides the ability to manually update file hashes and remove files from the monitoring database.

### Key Features:
- **File Hash Calculation**: Uses MD5 hashing to detect file modifications.
- **Pop-up Notifications**: Shows notifications for any modified files.
- **Database Management**: Stores file paths, hashes, and timestamps in a JSON database.
- **Continuous Monitoring**: Periodically checks for file integrity and updates the database with new hashes.
- **Manual Operations**: Allows adding/removing files, and manually updating file hashes through an interactive CLI.

---

## Main Code Parts

### 1. **Database Management**:
This part of the code manages a local JSON database (`hash_database.json`) to store file paths, their corresponding hash values, and timestamps.

```python
DATABASE_FILE = "hash_database.json"

# Load existing database or create a new one
def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    return {}

# Save the updated database
def save_database(database):
    with open(DATABASE_FILE, "w") as f:
        json.dump(database, f, indent=4)
```

### 2. File Management (`file.py`)

This script provides a command-line interface for managing monitored files.

```python
def add_file(filepath, database):
    if os.path.exists(filepath):
        file_hash = calculate_file_hash(filepath)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        database[filepath] = [{"hash": file_hash, "timestamp": current_time}]
        print(f"File {filepath} added to monitoring list.")
    else:
        print(f"File {filepath} does not exist.")
```

- **Add Files**: Users can add files to the monitoring list.
- **Update Hashes**: Users can manually save new hashes for monitored files.

### 3. Notification System

```python
def show_notification(filepath):
    root = Tk()
    root.withdraw()
    messagebox.showinfo("File Integrity Alert", f"File modified: {filepath}")
    root.destroy()
```

- **GUI Alerts**: Displays pop-ups for file modifications.
- **Sequential Alerts**: Ensures all modified files are notified with a 5-second gap.

---

## Usage

1. **Add Files to Monitor**:
   Run `file.py` to add files to the monitoring database:
   ```bash
   python file.py
   ```

2. **Start Monitoring**:
   Run `int.py` to monitor files and receive alerts for modifications:
   ```bash
   python int.py
   ```

3. **Pop-Up Alerts**:
   If any file is modified, pop-up notifications will appear sequentially for each affected file.

---

## Customization

- **Adjust Monitoring Interval**: Change `time.sleep(30)` in `int.py` for the interval between scans.
- **Change Notification Gap**: Modify `time.sleep(5)` in `int.py` to adjust the delay between notifications.

---

## Contributing

Feel free to fork this repository, open issues, or submit pull requests for improvements!

## License

This project is licensed under the MIT License.
```

This version provides an easy-to-follow explanation of the tool's functionality, key code snippets, and usage, making it suitable for your GitHub repository.

