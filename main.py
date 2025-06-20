from password_manager.auth import authenticate

def main():
    if authenticate():
        print("Vault unlocked. You can now perform password manager operations.")
        # CLI functionality to be added here in feature/cli branch
    else:
        print("Authentication failed. Exiting...")

if __name__ == "__main__":
    main()
