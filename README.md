# OS Project - Secure Backup & Restore System

This project implements a comprehensive backup and restore system using Python and Flask, with features like optional compression, encryption, decryption. It applies key Operating System concepts including file management, process synchronization, memory optimization, and error handling.

## 🔍 Problem Statement
Design a comprehensive backup system that allows users to:
- Specify files and directories for backup.
- Optionally compress and encrypt backup data.
- Restore data when needed securely and efficiently.

## 🎯 Objectives
- Backup and restore user-specified files/directories.
- Provide optional compression for storage efficiency.
- Provide optional encryption for data security.
- Ensure seamless decryption during restore.

## 🧠 OS Concepts Applied
- **File Management**: Copying, compressing, encrypting files.
- **Process Synchronization**: Avoid data conflicts during concurrent operations.
- **Error Handling**: Handle I/O exceptions to maintain data integrity.
- **Memory Management**: Optimize usage during compression/encryption.
- **Deadlock Prevention**: Prevent resource conflicts in multi-threaded tasks.

## 🛠️ Tech Stack
- **Language**: Python 3.12
- **Web Framework**: Flask
- **Frontend**: HTML, CSS
- **Libraries Used**:
  - `shutil` for file operations
  - `cryptography` for encryption
  - `zipfile` for compression

## 📁 Project Structure

<pre>
  ├── static/
│ ├── logo1.png
│ └── sky.jpg
├── templates/
│ ├── backup.html
│ ├── forget_password.html
│ ├── home.html
│ ├── login.html
│ ├── pop.html
│ ├── reset_password.html
│ ├── restore.html
│ ├── verify_otp.html
│ └── welcome.html
├── app.py
├── backup.py
└── restore.py
</pre>

## 🚀 Future Enhancements
- Support for **cloud-based backups**.
- Implement **automated/scheduled backups**.
- Upgrade to **AES encryption** for stronger security.
- Improve **UI/UX** with drag-and-drop file selection.
- Add **multi-platform support** (Windows, macOS, Linux).

## 👨‍💻 Author

- **Paranthagan S**  
