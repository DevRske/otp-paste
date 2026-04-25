import json
import time
from pathlib import Path

import keyboard
import keyring
import pyautogui
import pyotp

DEFAULT_HOTKEY = "ctrl+alt+a"
CONFIG_PATH = Path(__file__).with_name("config.json")
PYAUTOGUI_KEY_MAP = {
    "control": "ctrl",
    "left ctrl": "ctrlleft",
    "right ctrl": "ctrlright",
    "left alt": "altleft",
    "right alt": "altright",
    "left shift": "shiftleft",
    "right shift": "shiftright",
    "windows": "win",
    "left windows": "winleft",
    "right windows": "winright",
}


def load_hotkey():
    if not CONFIG_PATH.exists():
        return DEFAULT_HOTKEY

    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Warning: Failed to read {CONFIG_PATH.name}: {exc}")
        print(f"Falling back to default hotkey: {DEFAULT_HOTKEY}")
        return DEFAULT_HOTKEY

    hotkey = config.get("hotkey", DEFAULT_HOTKEY)
    if not isinstance(hotkey, str) or not hotkey.strip():
        print(f"Warning: Invalid hotkey in {CONFIG_PATH.name}.")
        print(f"Falling back to default hotkey: {DEFAULT_HOTKEY}")
        return DEFAULT_HOTKEY

    return hotkey.strip().lower()


def release_hotkey_keys(hotkey):
    for key in hotkey.split("+"):
        normalized_key = key.strip().lower()
        if not normalized_key:
            continue

        pyautogui_key = PYAUTOGUI_KEY_MAP.get(normalized_key, normalized_key)
        try:
            pyautogui.keyUp(pyautogui_key)
        except Exception:
            continue


def type_my_code(hotkey):
    secret = keyring.get_password("AuthApp", "MySecretKey")
    if not secret:
        print("Error: Secret not found in Windows. Run setup_secrets.py first.")
        return

    time.sleep(0.2)
    release_hotkey_keys(hotkey)

    pyautogui.click()
    totp = pyotp.TOTP(secret)
    pyautogui.write(totp.now())


HOTKEY = load_hotkey()

print(f"Authenticator is running! Press {HOTKEY} to type your code.")
print("Close this window to stop the script.")

keyboard.add_hotkey(HOTKEY, lambda: type_my_code(HOTKEY))
keyboard.wait()
