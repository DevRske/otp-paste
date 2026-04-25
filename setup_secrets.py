import keyring
import getpass

print("=== Authenticator Setup ===")
print("Please get your TOTP Secret Key.")

secret = getpass.getpass("Paste your Secret Key (text will be hidden): ")

if secret.strip():
    # Windows Credential Manager
    keyring.set_password("AuthApp", "MySecretKey", secret.strip())
    print("Success! Secret saved securely to Windows.")
else:
    print("No secret entered.")