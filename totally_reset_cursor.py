import os
import shutil
import platform
import time
import uuid
import subprocess
from colorama import Fore, Style, init

init()

EMOJI = {
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "RESET": "🔄",
    "MENU": "📋",
    "WARNING": "⚠️"
}

def delete_directory(path, translator=None):
    """Deletes a directory and all its contents."""
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('totally_reset.removed', path=path)}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('totally_reset.failed_to_remove', path=path, error=e)}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('totally_reset.not_found', path=path)}{Style.RESET_ALL}")

def delete_file(path, translator=None):
    """Deletes a file if it exists."""
    if os.path.isfile(path):
        try:
            os.remove(path)
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('totally_reset.removed', path=path)}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('totally_reset.failed_to_remove', path=path, error=e)}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}{EMOJI['INFO']} {translator.get('totally_reset.not_found', path=path)}{Style.RESET_ALL}")

def reset_machine_id(translator=None):
    """Resets the machine ID to a new UUID."""
    new_id = str(uuid.uuid4())
    if platform.system() == "Windows":
        try:
            subprocess.run(
                ["reg", "add", "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography", "/v", "MachineGuid", "/d", new_id, "/f"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('totally_reset.machine_guid_reset', new_id=new_id)}{Style.RESET_ALL}")
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('totally_reset.failed_to_reset_machine_guid', error=e)}{Style.RESET_ALL}")
    elif platform.system() == "Linux":
        machine_id_paths = ["/etc/machine-id", "/var/lib/dbus/machine-id"]
        for path in machine_id_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'w') as f:
                        f.write(new_id)
                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('totally_reset.machine_id_reset', path=path)}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('totally_reset.failed_to_reset_machine_id', path=path, error=e)}{Style.RESET_ALL}")
    elif platform.system() == "Darwin":  # macOS
        print("ℹ️ macOS does not use a machine-id file. Skipping machine ID reset.")
    else:
        print(f"{Fore.RED}{EMOJI['ERROR']} {translator.get('totally_reset.unsupported_os')}{Style.RESET_ALL}")

def display_features_and_warnings(translator=None):
    """Displays features and warnings before proceeding."""
    print(f"\n{Fore.GREEN}{EMOJI['MENU']} {translator.get('totally_reset.title')}")
    print("=====================================")
    print(f"{translator.get('totally_reset.feature_title')}")
    print(f"{Fore.GREEN}{translator.get('totally_reset.feature_1')}")
    print(f"{Fore.GREEN}{translator.get('totally_reset.feature_2')}")
    print(f"{Fore.GREEN}{translator.get('totally_reset.feature_3')}")
    print(f"{Fore.GREEN}{translator.get('totally_reset.feature_4')}")
    print(f"{Fore.GREEN}{translator.get('totally_reset.feature_5')}")
    print(f"{Fore.GREEN}{translator.get('totally_reset.feature_6')}")
    print(f"{Fore.GREEN}{translator.get('totally_reset.feature_7')}")
    print(f"{Fore.GREEN}{translator.get('totally_reset.feature_8')}")
    print(f"{Fore.GREEN}{translator.get('totally_reset.feature_9')}")
    print(f"\n{Fore.YELLOW}{EMOJI['WARNING']} {translator.get('totally_reset.warning_title')}")
    print(f"{Fore.YELLOW}{translator.get('totally_reset.warning_1')}")
    print(f"{Fore.YELLOW}{translator.get('totally_reset.warning_2')}")
    print(f"{Fore.YELLOW}{translator.get('totally_reset.warning_3')}")
    print(f"{Fore.YELLOW}{translator.get('totally_reset.warning_4')}")
    print(f"{Fore.YELLOW}{translator.get('totally_reset.warning_5')}")
    print(f"{Fore.YELLOW}{translator.get('totally_reset.warning_6')}")
    print(f"{Fore.YELLOW}{translator.get('totally_reset.warning_7')}")
    print("=====================================\n")

def get_user_confirmation(translator=None):
    """Prompts the user for confirmation to proceed."""
    while True:
        response = input(f"{Fore.YELLOW} {translator.get('totally_reset.confirm_title')} {translator.get('totally_reset.invalid_choice')}: ").lower().strip()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print(f"{Fore.RED}{translator.get('totally_reset.invalid_choice')}{Style.RESET_ALL}")

def reset_cursor(translator=None):
    print(f"\n{Fore.GREEN}{EMOJI['RESET']} {translator.get('totally_reset.resetting_cursor')}\n")

    # Platform-specific paths
    paths = []
    if platform.system() == "Linux":
        paths = [
            os.path.expanduser("~/.cursor"),
            os.path.expanduser("~/.local/share/cursor"),
            os.path.expanduser("~/.config/cursor"),
            os.path.expanduser("~/.cache/cursor"),
            "/usr/local/bin/cursor",
            "/opt/cursor",
            "/usr/bin/cursor",
            os.path.expanduser("~/.cursor/machine-id.db"),
            os.path.expanduser("~/.local/share/Cursor"),
            os.path.expanduser("~/.config/Cursor"),
            os.path.expanduser("~/.cache/Cursor")
        ]
    elif platform.system() == "Darwin":  # macOS
        paths = [
            os.path.expanduser("~/Library/Application Support/Cursor"),
            os.path.expanduser("~/Library/Caches/Cursor"),
            "/Applications/Cursor.app",
            os.path.expanduser("~/Library/Preferences/com.cursor.app.plist"),
        ]
    elif platform.system() == "Windows":
        paths = [
            os.path.expanduser("~\\AppData\\Local\\Cursor"),
            os.path.expanduser("~\\AppData\\Roaming\\Cursor"),
            os.path.expanduser("~\\.cursor"),
            os.path.expanduser("~\\.config\\Cursor"),
            os.path.expanduser("~\\.cache\\Cursor"),
            "C:\\Program Files\\Cursor",
            "C:\\Program Files (x86)\\Cursor",
            "C:\\Users\\%USERNAME%\\AppData\\Local\\Cursor",
            "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Cursor",
        ]

    # Remove directories
    for path in paths:
        delete_directory(path, translator)

    # Remove common files related to Cursor
    files = [
        os.path.expanduser("~/.cursor/machine-id.db"),
        os.path.expanduser("~/.local/share/cursor.db"),
        os.path.expanduser("~/.config/cursor/preferences.json"),
        os.path.expanduser("~/.cache/cursor.log"),
    ]

    for file in files:
        delete_file(file, translator)

    # Extra cleanup (wildcard search)
    print(f"\n{Fore.YELLOW}{EMOJI['INFO']} {translator.get('totally_reset.deep_scanning')}")
    base_dirs = ["/tmp", "/var/tmp", os.path.expanduser("~")]  # Linux and macOS
    if platform.system() == "Windows":
        base_dirs = ["C:\\Temp", "C:\\Windows\\Temp", os.path.expanduser("~")]  # Windows

    for base in base_dirs:
        for root, dirs, files in os.walk(base):
            for dir in dirs:
                if "cursor" in dir.lower():
                    delete_directory(os.path.join(root, dir), translator)
            for file in files:
                if "cursor" in file.lower():
                    delete_file(os.path.join(root, file), translator)

    # Reset machine ID
    reset_machine_id(translator)

    print(f"\n{Fore.GREEN}{EMOJI['SUCCESS']} {translator.get('totally_reset.cursor_reset_completed')}")

def main(translator=None):
    start_time = time.time()
    
    # Display features and warnings
    display_features_and_warnings(translator)
    
    # Get user confirmation
    if get_user_confirmation(translator):
        reset_cursor(translator)
        end_time = time.time()
        print(f"\n{Fore.GREEN}⏱️ {translator.get('totally_reset.completed_in', time=f'{end_time - start_time:.2f} seconds')}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}❌ {translator.get('totally_reset.operation_cancelled')}{Style.RESET_ALL}")

if __name__ == '__main__':
    from main import translator
    main(translator)
