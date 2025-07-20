import zipfile
import os
import shutil
from cryptography.fernet import Fernet

def package_as_docx(folder_path, output_docx):
    """Package the extracted Word document structure back into a .docx file."""
    with zipfile.ZipFile(output_docx, 'w') as docx_zip:
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                # To maintain correct folder structure inside the zip file
                relative_path = os.path.relpath(file_path, folder_path)
                docx_zip.write(file_path, relative_path)

def perform_restore(backup_file, restore_location, decrypt=False, key=None):
    # Ensure restore location exists
    if not os.path.exists(restore_location):
        os.makedirs(restore_location)

    # Handle directory restoration
    if os.path.isdir(backup_file):
        if decrypt and key:
            key_bytes = key.encode()
            cipher_suite = Fernet(key_bytes)
            decrypted_dir = os.path.join(os.path.dirname(backup_file), f'decrypted_{os.path.basename(backup_file)}')
            os.makedirs(decrypted_dir, exist_ok=True)

            for root, dirs, files in os.walk(backup_file):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    relative_path = os.path.relpath(root, backup_file)
                    dest_dir = os.path.join(decrypted_dir, relative_path)
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    dest_file_path = os.path.join(dest_dir, file_name)
                    
                    with open(file_path, 'rb') as file:
                        encrypted_data = file.read()
                    
                    decrypted_data = cipher_suite.decrypt(encrypted_data)
                    
                    with open(dest_file_path, 'wb') as file:
                        file.write(decrypted_data)
            
            shutil.copytree(decrypted_dir, os.path.join(restore_location, os.path.basename(backup_file)), dirs_exist_ok=True)
            shutil.rmtree(decrypted_dir)

        else:
            shutil.copytree(backup_file, os.path.join(restore_location, os.path.basename(backup_file)), dirs_exist_ok=True)

    # Handle file restoration
    else:
        if decrypt and key:
            cipher_suite = Fernet(key)
            
            with open(backup_file, 'rb') as file:
                encrypted_data = file.read()
            
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            
            temp_file_path = os.path.join(os.path.dirname(backup_file), f'decrypted_{os.path.basename(backup_file)}')
            with open(temp_file_path, 'wb') as file:
                file.write(decrypted_data)
            
            backup_file = temp_file_path

        # If it's a ZIP file, handle as an archive (such as .docx)
        if zipfile.is_zipfile(backup_file):
            with zipfile.ZipFile(backup_file, 'r') as zip_ref:
                extract_folder = os.path.join(restore_location, os.path.splitext(os.path.basename(backup_file))[0])
                zip_ref.extractall(extract_folder)
                
                # Check if it's a Word document structure and repackage it as .docx
                if os.path.exists(os.path.join(extract_folder, 'word')) and os.path.exists(os.path.join(extract_folder, '[Content_Types].xml')):
                    output_docx = os.path.join(restore_location, os.path.basename(backup_file).replace('.zip', '.docx'))
                    package_as_docx(extract_folder, output_docx)
                    shutil.rmtree(extract_folder)  # Clean up the extracted folder

        else:
            # Copy regular file
            try:
                shutil.copy(backup_file, os.path.join(restore_location, os.path.basename(backup_file)))
            except OSError as e:
                raise e

        # Clean up temporary decrypted file
        if decrypt and key and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
