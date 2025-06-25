from password_manager.auth import authenticate, derive_key
from password_manager.cli import run_cli

def main():
    print("🔐 Welcome to Password Manager CLI")
    
    if authenticate():
        master_password = input("Re-enter Master Password to unlock vault: ")
        key = derive_key(master_password)
        run_cli(key)  # Pass the derived key to CLI after successful auth
    else:
        print("Authentication failed. Exiting...")

if __name__ == "__main__":
    main()
