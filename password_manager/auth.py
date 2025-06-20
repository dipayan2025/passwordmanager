import os
import base64
import getpass
from cryptography.fernet import Fernet, InvalidToken
from password_manager import config

def derive_key(password: str) -> bytes:
    """Derives a Fernet-compatible key from the provided password."""
    return base64.urlsafe_b64encode(password.encode('utf-8').ljust(32, b'0'))

def set_master_password() -> bool:
    """Sets the master password on first run."""
    if os.path.exists(config.VAULT_KEY_PATH):
        print("Master password already set.")
        return False

    password = getpass.getpass("Set Master Password: ")
    confirm = getpass.getpass("Confirm Master Password: ")

    if password != confirm:
        print("Passwords do not match.")
        return False  # Return False to indicate failure

    key = derive_key(password)

    # Save the derived key
    with open(config.VAULT_KEY_PATH, 'wb') as key_file:
        key_file.write(key)

    # Save encrypted test message for verification
    cipher = Fernet(key)
    test_token = cipher.encrypt(b'test')
    with open(config.TEST_FILE_PATH, 'wb') as test_file:
        test_file.write(test_token)

    print("Master password set successfully.")
    return True  # Return True to indicate success


def verify_master_password() -> bool:
    """Verifies the entered master password."""
    if not os.path.exists(config.VAULT_KEY_PATH):
        print("No master password set. Please set it first.")
        return False

    password = getpass.getpass("Enter Master Password: ")
    key = derive_key(password)
    cipher = Fernet(key)

    try:
        with open(config.TEST_FILE_PATH, 'rb') as test_file:
            encrypted_test = test_file.read()

        # Decrypt and verify
        decrypted = cipher.decrypt(encrypted_test)
        if decrypted == b'test':
            print("Access granted.")
            return True
    except (InvalidToken, Exception):
        pass

    print("Invalid Master Password.")
    return False

def authenticate() -> bool:
    """Handles first-time setup or master password verification."""
    if not os.path.exists(config.VAULT_KEY_PATH):
        print("First run detected. Please set your master password.")
        return set_master_password()  # Now returns True or False
    else:
        return verify_master_password()

