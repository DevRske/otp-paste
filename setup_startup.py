import os
import sys
import winreg

# winreg path for startup
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "AuthenticatorApp"

def get_script_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "authenticator_cli.py")

def get_pythonw_path():
    python_exe = sys.executable
    return python_exe.replace("python.exe", "pythonw.exe")

def enable_startup():
    script_path = get_script_path()
    pythonw_path = get_pythonw_path()
    
    command = f'"{pythonw_path}" "{script_path}"' # construct the cli command
    
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, APP_NAME, 0, winreg.REG_SZ, command)
        winreg.CloseKey(reg_key)
        print(f"\nEnabled.")
    except Exception as e:
        print(f"\nError: {e}")

def disable_startup():
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(reg_key, APP_NAME)
        winreg.CloseKey(reg_key)
        print(f"\nDisabled.")
    except FileNotFoundError:
        print("\nError: not found in registry (probably wasn't enabled in the first place).")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    print("=== Startup Manager ===")
    print("1. Enable auto-start on boot")
    print("2. Disable auto-start")
    
    choice = input("Select option (1 or 2): ").strip()
    
    if choice == '1':
        enable_startup()
    elif choice == '2':
        disable_startup()
    else:
        print("Invalid choice.")