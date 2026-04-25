import json
import logging
import time
from pathlib import Path

import keyboard
import keyring
import pyautogui
import pyotp

DEFAULT_HOTKEY = "ctrl+alt+a"
CONFIG_PATH = Path(__file__).with_name("config.json")
LOG_PATH = Path(__file__).with_name("authenticator.log")
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
MODIFIER_KEYS = {
    "ctrl",
    "control",
    "alt",
    "shift",
    "windows",
    "left ctrl",
    "right ctrl",
    "left alt",
    "right alt",
    "left shift",
    "right shift",
    "left windows",
    "right windows",
}

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
LOGGER = logging.getLogger(__name__)


def validate_hotkey(hotkey):
    normalized_hotkey = hotkey.strip().lower()
    keyboard.parse_hotkey_combinations(normalized_hotkey)
    return normalized_hotkey


def fallback_to_default_hotkey(reason):
    message = f"Warning: {reason}"
    print(message)
    LOGGER.warning(message)
    fallback_message = f"Falling back to default hotkey: {DEFAULT_HOTKEY}"
    print(fallback_message)
    LOGGER.warning(fallback_message)

    try:
        return validate_hotkey(DEFAULT_HOTKEY)
    except (AttributeError, TypeError, ValueError) as exc:
        fatal_message = f"Error: Default hotkey '{DEFAULT_HOTKEY}' is invalid."
        print(fatal_message)
        LOGGER.error("%s %s", fatal_message, exc)
        raise RuntimeError(fatal_message) from exc


def load_hotkey():
    if not CONFIG_PATH.exists():
        return validate_hotkey(DEFAULT_HOTKEY)

    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fallback_to_default_hotkey(f"Failed to read {CONFIG_PATH.name}: {exc}")

    hotkey = config.get("hotkey", DEFAULT_HOTKEY)
    if not isinstance(hotkey, str) or not hotkey.strip():
        return fallback_to_default_hotkey(f"Invalid hotkey in {CONFIG_PATH.name}.")

    try:
        return validate_hotkey(hotkey)
    except (AttributeError, TypeError, ValueError) as exc:
        return fallback_to_default_hotkey(
            f"Failed to parse hotkey '{hotkey}' from {CONFIG_PATH.name}: {exc}"
        )


def release_hotkey_keys(hotkey):
    for key in hotkey.split("+"):
        normalized_key = key.strip().lower()
        if not normalized_key or normalized_key not in MODIFIER_KEYS:
            continue

        pyautogui_key = PYAUTOGUI_KEY_MAP.get(normalized_key, normalized_key)
        try:
            pyautogui.keyUp(pyautogui_key)
        except Exception:
            continue


def type_my_code(hotkey):
    try:
        secret = keyring.get_password("AuthApp", "MySecretKey")
        if not secret:
            message = "Error: Secret not found in Windows. Run setup_secrets.py first."
            print(message)
            LOGGER.error(message)
            return

        time.sleep(0.2)
        release_hotkey_keys(hotkey)

        pyautogui.click()
        totp = pyotp.TOTP(secret)
        pyautogui.write(totp.now())
        LOGGER.info("Typed a TOTP code successfully.")
    except Exception:
        LOGGER.exception("Failed to type a TOTP code.")


HOTKEY = load_hotkey()

print(f"Authenticator is running! Press {HOTKEY} to type your code.")
print("Close this window to stop the script.")
LOGGER.info("Authenticator started with hotkey: %s", HOTKEY)

try:
    keyboard.add_hotkey(
        HOTKEY,
        lambda: type_my_code(HOTKEY),
        suppress=False,
        trigger_on_release=True,
    )
except Exception:
    LOGGER.exception("Failed to register hotkey: %s", HOTKEY)
    raise

keyboard.wait()
