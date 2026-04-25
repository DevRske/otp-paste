import getpass
import keyring
import pyotp


def normalize_secret(secret):
    return "".join(secret.split())


def is_valid_secret(secret):
    try:
        pyotp.TOTP(secret).now()
    except Exception:
        return False

    return True

print("=== Authenticator Setup ===")
print("Please get your TOTP Secret Key.")

secret = getpass.getpass("Paste your Secret Key (text will be hidden): ")
normalized_secret = normalize_secret(secret)

if normalized_secret:
    if not is_valid_secret(normalized_secret):
        print("Invalid TOTP secret. Nothing was saved.")
    else:
        keyring.set_password("AuthApp", "MySecretKey", normalized_secret)
        print("Success! Secret saved securely to Windows.")
else:
    print("No secret entered.")
