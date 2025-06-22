from password_manager.auth import authenticate
from password_manager.cli import run_cli  # Your CLI function (to be developed)

def main():
    if authenticate():
        print("Vault unlocked. You can now perform password manager operations.")
        run_cli()  # CLI actions now only accessible after successful auth
    else:
        print("Authentication failed. Exiting...")

if __name__ == "__main__":
    main()
