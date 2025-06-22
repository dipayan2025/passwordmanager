from password_manager import vault, config
from password_manager.auth import derive_key

def run_cli():
    """Simple CLI for password manager (called after successful authentication)."""
    master_password = input("Re-enter Master Password to derive vault key: ")
    key = derive_key(master_password)

    
    vault_data = vault.decrypt_vault(key)

    while True:
        print("\n--- Password Manager CLI ---")
        print("1. Add Credential")
        print("2. View Vault")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            site = input("Site: ")
            username = input("Username: ")
            password = input("Password: ")

            vault_data[site] = {"username": username, "password": password}
            vault.encrypt_vault(vault_data, key)  

            print(f"Credential for {site} saved successfully.")

        elif choice == "2":
            if not vault_data:
                print("Vault is empty.")
            else:
                for site, creds in vault_data.items():
                    print(f"Site: {site}, Username: {creds['username']}, Password: {creds['password']}")

        elif choice == "3":
            print("Exiting Password Manager CLI.")
            break
        else:
            print("Invalid option. Try again.")
