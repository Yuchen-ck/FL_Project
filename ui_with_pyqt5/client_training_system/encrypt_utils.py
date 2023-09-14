import shutil
from cryptography.fernet import Fernet

def file_encrypt(key, original_file, encrypted_file):
        
    f = Fernet(key)
    
    with open(original_file, 'rb') as file:
        original = file.read()

    encrypted = f.encrypt(original)

    with open (encrypted_file, 'wb') as file:
        file.write(encrypted)

# Delete the specific folder!!!
def delete_UsedFolder(deleteFolderPath):
    delete_dir = deleteFolderPath
    try:
        shutil.rmtree(delete_dir)
    except OSError as e:
        print(f"Error:{ e.strerror}")
    
    return "刪除非空資料夾."