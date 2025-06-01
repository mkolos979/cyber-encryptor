from cryptography.fernet import Fernet
import os

def generate_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    if os.path.exists('key.key'):
        with open('key.key', 'rb') as key_file:
            return key_file.read()

    else:
        return generate_key()

def encrypt_file(file_path):
    key = load_key()
    cipher = Fernet(key)

    with open(file_path, 'rb') as f:
        data = f.read()

    encrypted = cipher.encrypt(data)
    encrypted_path = file_path + '.enc'   

    with open(encrypted_path, 'wb') as f:
        f.write(encrypted)

    os.remove(file_path)

    return encrypted_path     

def decrypt_file(file_path):
    key = load_key()
    cipher = Fernet(key)

    with open(file_path, 'rb') as f:
        data = f.read()

    decrypted = cipher.decrypt(data)
    original_path = file_path.replace('.enc', '')

    with open(original_path, 'wb') as f:
        f.write(decrypted)

    os.remove(file_path)

    return original_path