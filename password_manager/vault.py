import os
import json
from cryptography.fernet import Fernet
from hashlib import sha256
import base64
from password_manager import config


VAULT_FILE = "data/vault.enc"

def derive_key(master_password):
    """Derive a Fernet key from the master password using SHA-256."""
    hashed = sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)

def encrypt_vault(data, key):
    """Encrypt the vault data dictionary."""
    fernet = Fernet(key)
    json_data = json.dumps(data).encode()
    encrypted = fernet.encrypt(json_data)

    
    os.makedirs(os.path.dirname(VAULT_FILE), exist_ok=True)

    with open(VAULT_FILE, 'wb') as f:
        f.write(encrypted)
    # Also save a readable version for testing/debugging (optional)
    with open(config.VAULT_JSON_PATH, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def decrypt_vault(key):
    """Decrypt the vault data, returning it as a Python dictionary."""
    if not os.path.exists(VAULT_FILE):
        return {}  
    with open(VAULT_FILE, 'rb') as f:
        encrypted = f.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted)
    return json.loads(decrypted.decode())
