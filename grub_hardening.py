import os
import re

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

def run():
    """Main function to apply GRUB hardening."""
    update_grub_file()
    regenerate_grub()

if __name__ == "__main__":
    run()
