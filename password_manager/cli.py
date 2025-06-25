def run_cli(key):
    from password_manager import vault

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
            print(f"✅ Saved: {site}")

        elif choice == "2":
            if not vault_data:
                print("Vault is empty.")
            else:
                for site, creds in vault_data.items():
                    print(f"{site}: {creds['username']} | {creds['password']}")

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid option.")
