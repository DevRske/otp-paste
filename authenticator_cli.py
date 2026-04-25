import pyotp
import pyautogui
import keyboard
import keyring
import time

def type_my_code():
    secret = keyring.get_password("AuthApp", "MySecretKey")
    if not secret:
        print("Error: Secret not found in Windows. Run setup.py first.")
        return 

    time.sleep(0.2)
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('alt')
    pyautogui.keyUp('a') 

    pyautogui.click()
    totp = pyotp.TOTP(secret)
    pyautogui.write(totp.now())

print("Authenticator is running! Press Ctrl+Alt+A to type your code.")
print("Close this window to stop the script.")

keyboard.add_hotkey('ctrl+alt+a', type_my_code)
keyboard.wait()