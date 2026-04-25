# OTP Paste Helper

A small Windows utility that stores a TOTP secret in Windows Credential Manager and pastes the current 6-digit code with a global keyboard shortcut.

The project was initially built for Kaunas University of Technology (KTU) login systems, but it can also be used with other services that rely on standard TOTP authenticator codes.

## What It Does

- Stores your TOTP secret locally in Windows Credential Manager
- Generates the current code when needed
- Types the code into the active input field after pressing `Ctrl + Alt + A`

## Prerequisites

- Windows
- Python 3.x
- A service that uses standard TOTP-based 2FA

## Getting Your TOTP Secret

This tool needs the raw TOTP secret, not just the 6-digit code shown in an authenticator app.

### General Method

For many services, the secret is shown during 2FA setup as either:

- a QR code
- a manual setup key
- or a URI containing `secret=...`

If the site shows a QR code only, you can scan it with a QR reader and copy the value after `secret=` from the resulting OTP URI.

Example:

```text
otpauth://totp/Example:email@example.com?secret=ABC123...
```

In that case, the part after `secret=` is the value this script needs.

### KTU-Specific Notes

KTU was the original target for this project. In KTU systems, getting the secret may require starting the authenticator setup again from the login portal.

Important: re-setting up the authenticator can generate a new secret and invalidate the one currently stored in your mobile authenticator app. If you do this, make sure you also scan the newly generated QR code with your phone so you do not lose access.

Typical KTU flow:

1. Log in to the KTU system.
2. When prompted for the authenticator code, choose the option to re-set up the authenticator.
3. Read the QR code with a QR scanner.
4. Copy the value after `secret=`.
5. Also add the new QR code to your authenticator app.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Store your secret securely:

```bash
python setup_secrets.py
```

This saves the secret to Windows Credential Manager.

3. Optional: adjust the hotkey in `config.json`:

```json
{
  "hotkey": "ctrl+alt+a"
}
```

Change the value to any shortcut format supported by the Python `keyboard` library, for example:

- `ctrl+alt+a`
- `ctrl+shift+v`
- `alt+q`

## Usage

### Run Manually

```bash
python authenticator_cli.py
```

The script will stay running and listen for the hotkey defined in `config.json`.

### Start Automatically With Windows

```bash
python setup_startup.py
```

This lets you enable or disable launching the script automatically at login.

### Paste a Code

While the script is running:

1. Open the page or app where the TOTP code is required.
2. Place the cursor in the code input field.
3. Press your configured hotkey.

The current TOTP code will be generated and typed automatically.
