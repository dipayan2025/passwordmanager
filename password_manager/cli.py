import time
from password_manager import vault
from password_manager.generator import generate_password
import pyperclip

INACTIVITY_TIMEOUT = 120  # seconds

def run_cli(key):
    vault_data = vault.decrypt_vault(key)
    last_active = time.time()

    while True:
        # Check inactivity timeout
        if time.time() - last_active > INACTIVITY_TIMEOUT:
            print("🔒 Session timed out. Please log in again.")
            break

        print("\n--- Password Manager CLI ---")
        print("1. Add Credential")
        print("2. View All Credentials")
        print("3. Get Credential by Site")
        print("4. Edit Credential")
        print("5. Delete Credential")
        print("6. Generate Password")
        print("7. Search Credentials")
        print("8. Exit")

        choice = input("Select an option: ").strip()
        last_active = time.time()  # reset timer on interaction

        if choice == "1":
            site = input("Site: ")
            username = input("Username: ")
            password = input("Password: ")
            vault_data[site] = {"username": username, "password": password}
            vault.encrypt_vault(vault_data, key)
            print(f"✅ Saved: {site}")

        elif choice == "2":
            if not vault_data:
                print("Vault is empty.")
            else:
                for site, creds in vault_data.items():
                    print(f"{site}: {creds['username']} | {creds['password']}")
        elif choice == "3":
            site = input("Enter site name: ")
            if site in vault_data:
                creds = vault_data[site]
                print(f"{site} → {creds['username']} | {creds['password']}")
                copy = input("Copy password to clipboard? (y/n): ").lower()
                if copy == 'y':
                    pyperclip.copy(creds['password'])
                    print("📋 Password copied to clipboard.")
            else:
                print("❌ Site not found.")

        elif choice == "4":
            site = input("Site to edit: ")
            if site in vault_data:
                username = input("New username (leave blank to keep current): ")
                password = input("New password (leave blank to keep current): ")
                if username:
                    vault_data[site]['username'] = username
                if password:
                    vault_data[site]['password'] = password
                vault.encrypt_vault(vault_data, key)
                print(f"✏️ Updated: {site}")
            else:
                print("❌ Site not found.")

        elif choice == "5":
            site = input("Site to delete: ")
            if site in vault_data:
                del vault_data[site]
                vault.encrypt_vault(vault_data, key)
                print(f"🗑️ Deleted: {site}")
            else:
                print("❌ No such site.")

        elif choice == "6":
            site = input("Site to save password for: ")
            username = input("Username: ")
            length = int(input("Password length: "))
            use_symbols = input("Include symbols? (y/n): ").lower() == 'y'
            use_numbers = input("Include numbers? (y/n): ").lower() == 'y'
            use_uppercase = input("Include uppercase? (y/n): ").lower() == 'y'

            password = generate_password(length, use_symbols, use_numbers, use_uppercase)
            print(f"🔐 Generated Password: {password}")

            save = input("Auto-save this to vault? (y/n): ").lower()
            if save == 'y':
                vault_data[site] = {"username": username, "password": password}
                vault.encrypt_vault(vault_data, key)
                print(f"✅ Saved {site} with generated password.")


        elif choice == "7":
            query = input("Search by site or username: ").lower()
            found = False
            for site, creds in vault_data.items():
                if query in site.lower() or query in creds['username'].lower():
                    print(f"{site}: {creds['username']} | {creds['password']}")
                    found = True
            if not found:
                print("❌ No match found.")

        elif choice == "8":
            print("🔒 Exiting Password Manager.")
            break

        else:
            print("❌ Invalid option. Try again.")
