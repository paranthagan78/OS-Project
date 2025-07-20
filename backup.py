import os
import shutil
from cryptography.fernet import Fernet

def perform_backup(source, destination, compress=False, encrypt=False, password=None):
    # Ensure source and destination paths are properly formatted
    source = source.strip().strip("'").strip('"')
    destination = destination.strip().strip("'").strip('"')
    
    # Ensure the destination directory exists
    try:
        if not os.path.exists(destination):
            os.makedirs(destination)
    except Exception as e:
        print(f"Error creating directory: {e}")
        return

    # Copy the source to the destination directory
    try:
        if os.path.isfile(source):
            # Backup a single file
            backup_path = os.path.join(destination, os.path.basename(source))
            shutil.copy(source, backup_path)
            print(f"File backed up successfully from {source} to {destination}")
            
            if encrypt and password:
                # Encrypt the file
                key = Fernet.generate_key()
                cipher_suite = Fernet(key)
                
                with open(backup_path, 'rb') as file:
                    file_data = file.read()
                
                encrypted_data = cipher_suite.encrypt(file_data)
                
                with open(backup_path, 'wb') as file:
                    file.write(encrypted_data)
                
                # Optionally save or handle the key securely
                print(f"File encrypted. Key used: {key.decode()}")  # For debugging purposes only
                return key.decode()

        elif os.path.isdir(source):
            # Backup a directory
            backup_path = os.path.join(destination, os.path.basename(source))
            shutil.copytree(source, backup_path)
            print(f"Directory backed up successfully from {source} to {destination}")
            
            if encrypt and password:
                # Encrypt each file in the directory
                key = Fernet.generate_key()
                cipher_suite = Fernet(key)

                for root, dirs, files in os.walk(backup_path):
                    for file_name in files:
                        file_path = os.path.join(root, file_name)
                        
                        with open(file_path, 'rb') as file:
                            file_data = file.read()
                        
                        encrypted_data = cipher_suite.encrypt(file_data)
                        
                        with open(file_path, 'wb') as file:
                            file.write(encrypted_data)

                # Optionally save or handle the key securely
                print(f"Directory encrypted. Key used: {key.decode()}")  # For debugging purposes only
                return key.decode()

        else:
            print(f"Source does not exist or is not a file/directory: {source}")
    except Exception as e:
        print(f"Error during backup: {e}")
