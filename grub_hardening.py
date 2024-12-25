import os
import re
import subprocess

# Define a dictionary for GRUB hardening settings
grub_settings = {
    "GRUB_DEFAULT": "0",                       # Boot the default entry
    "GRUB_TIMEOUT": "5",                       # Set a timeout value (in seconds)
    "GRUB_HIDDEN_TIMEOUT": "0",                # Hide the menu timeout
    "GRUB_TERMINAL": "console",                # Use console for GRUB
    "GRUB_DISABLE_RECOVERY": "true",           # Disable recovery mode
    "GRUB_DISABLE_SUBMENU": "true",            # Disable submenus in the GRUB menu
    "GRUB_TERMINAL_INPUT": "console",          # Disallow keyboard input during boot menu
    "GRUB_CMDLINE_LINUX": "security=apparmor", # Example of adding security options to Linux boot args
    "GRUB_DISABLE_OS_PROBER": "true",          # Disable OS prober for additional OS's
    "GRUB_GFXMODE": "640x480",                # Use a low-resolution mode to avoid untrusted graphics
    "GRUB_PRELOAD_MODULES": "part_gpt part_msdos",  # Preload only necessary modules
    "GRUB_PICTURE": "",                       # Disable custom splash screen
    "GRUB_DISABLE_RECOVERY": "true",           # Disable recovery entries
    "GRUB_CMDLINE_LINUX_DEFAULT": "quiet splash security=apparmor"
}

# Path to the GRUB configuration file
grub_file_path = '/etc/default/grub'
grub_custom_file_path = '/etc/grub.d/40_custom'

def read_grub_file():
    """Reads the current /etc/default/grub file."""
    if not os.path.exists(grub_file_path):
        print(f"Error: {grub_file_path} does not exist.")
        return None
    
    with open(grub_file_path, 'r') as f:
        return f.readlines()

def write_grub_file(lines):
    """Writes the updated lines to /etc/default/grub."""
    with open(grub_file_path, 'w') as f:
        f.writelines(lines)

def update_grub_file():
    """Update the /etc/default/grub with the settings in grub_settings."""
    grub_file_lines = read_grub_file()
    if grub_file_lines is None:
        return
    
    updated = False
    # Loop over all settings in grub_settings and update the file contents
    for key, value in grub_settings.items():
        pattern = re.compile(rf'^{key}=(.*)', re.IGNORECASE)
        found = False
        
        for i, line in enumerate(grub_file_lines):
            if pattern.match(line):
                grub_file_lines[i] = f"{key}={value}\n"
                found = True
                updated = True
                break
        
        if not found:
            # If key doesn't exist in the file, add it to the end
            grub_file_lines.append(f"{key}={value}\n")
            updated = True

    if updated:
        write_grub_file(grub_file_lines)
        print("GRUB configuration updated.")
    else:
        print("No updates to GRUB configuration.")

def regenerate_grub():
    """Regenerate the GRUB configuration to apply the changes."""
    print("Regenerating GRUB config...")
    os.system('sudo update-grub')

def generate_grub_password_hash(password):
    """Generate a PBKDF2 hash of the password for GRUB."""
    try:
        # Run the grub-mkpasswd-pbkdf2 command to generate a hashed password
        result = subprocess.run(
            ['grub-mkpasswd-pbkdf2'],
            input=password.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        # Extract the hashed password from the command output
        output = result.stdout.decode()
        hash_line = [line for line in output.splitlines() if line.startswith('PBKDF2 hash of your password')][0]
        return hash_line.split(' is ')[1]
    except subprocess.CalledProcessError as e:
        print(f"Error generating password hash: {e}")
        return None


def add_grub_password_protection(password_hash):
    """Add GRUB password protection to /etc/grub.d/40_custom."""
    if not password_hash:
        print("No password hash provided. Skipping GRUB password protection.")
        return
    
    # Add the password hash to /etc/grub.d/40_custom
    try:
        with open(grub_custom_file_path, 'a') as f:
            f.write(f"\n# GRUB password protection\n")
            f.write(f"set superusers=\"root\"\n")
            f.write(f"password_pbkdf2 root {password_hash}\n")
        print("GRUB password protection added.")
    except IOError as e:
        print(f"Error updating {grub_custom_file_path}: {e}")

def run():
    """Main function to apply GRUB hardening and password protection."""
    
    # 1. Update GRUB settings
    update_grub_file()
    
    # 2. Ask the user for a password and generate the hash
    #password = input("Enter a password to secure GRUB (this will be hashed): ")
    #password_hash = generate_grub_password_hash(password)
    
    # 3. Add password protection to GRUB
    #add_grub_password_protection(password_hash)
    
    # 4. Regenerate GRUB
    #regenerate_grub()

if __name__ == "__main__":
    run()
