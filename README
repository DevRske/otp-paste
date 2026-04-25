# KTU TOTP Automator

A background utility designed to automate the entry of Time-Based One-Time Passwords (TOTP) for Kaunas University of Technology (KTU) login systems. This tool stores your secret key in the Windows Credential Manager and automatically inputs the current 6-digit code via a global keyboard shortcut.

## Important Notice: Secret Key Generation

To utilize this script, you must obtain your raw TOTP secret key from the KTU login portal.

**Warning:** Accessing the configuration to view the secret key requires initiating a "re-setup" of your authenticator app. This action generates a completely new secret key, rendering your existing mobile configuration defunct. You must scan the newly generated QR code with your mobile authenticator app simultaneously to ensure you retain access on your mobile device.

## Prerequisites

* Windows OS
* Python 3.x

## Setup Instructions

1. **Obtain the Secret Key:**
   * Navigate to the KTU login system and enter your login credentials.
   * When it asks to enter the auth code - select the option to re-setup your authenticator app.
   * Extract the raw text secret by scanning the QR code with a standard QR reader and copy the string immediately following \`secret=\`.
   * **Note:** You must also scan this new QR code with your mobile authenticator app.

2. **Install Dependencies:**
   \`\`\`
   pip install -r requirements.txt
   \`\`\`

3. **Store Credentials Securely:**
   Run the setup script. This will prompt you for your secret key and store it securely within the Windows Credential Manager.
   \`\`\`
   python setup_secrets.py
   \`\`\`

## Usage

### Manual Execution
Run the core script to start the listener in your current terminal session:
\`\`\`
python authenticator_cli.py
\`\`\`

### Automated Execution (Windows Startup)
To configure the application to launch silently in the background every time Windows boots, run the startup manager:
\`\`\`
python manage_startup.py
\`\`\`

### Triggering the Automation
While the application is running:
1. Navigate to the KTU login page.
2. Place your cursor in the TOTP input field.
3. Press \`Ctrl + Alt + A\`.

The application will instantly calculate the current 6-digit code and input it into the field.