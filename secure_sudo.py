import os
import subprocess
import stat

# Define paths
sudoers_path = '/etc/sudoers'
sudoers_d_path = '/etc/sudoers.d/'

# Ensure file is writable and remove immutable/append-only flags
def modify_file_flags(file_path):
    os.chmod(file_path, stat.S_IWUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)  # Make file writable
    try:
        subprocess.check_call(['chattr', '-i', '-a', file_path])  # Remove immutable and append-only flags
    except subprocess.CalledProcessError:
        print(f"Could not remove flags from {file_path}")

# Remove NOPASSWD lines from a file
def remove_nopasswd_lines(file_path):
    with open(file_path, 'r') as file:
        lines = [line for line in file if 'NOPASSWD' not in line]  # Filter out NOPASSWD lines

    with open(file_path, 'w') as file:
        file.writelines(lines)  # Write back the modified lines

# Fix file permissions
def fix_permissions(file_path):
    os.chmod(file_path, 0o440)  # Standard sudoers file permission

# Main processing function
def process_sudoers_files():
    # Process sudoers file
    if os.path.exists(sudoers_path):
        print(f"Processing {sudoers_path}")
        modify_file_flags(sudoers_path)
        remove_nopasswd_lines(sudoers_path)
        fix_permissions(sudoers_path)
    else:
        print(f"Error: {sudoers_path} not found.")

    # Process sudoers.d directory files
    if os.path.exists(sudoers_d_path):
        for filename in os.listdir(sudoers_d_path):
            file_path = os.path.join(sudoers_d_path, filename)
            if os.path.isfile(file_path):
                print(f"Processing {file_path}")
                modify_file_flags(file_path)
                remove_nopasswd_lines(file_path)
                fix_permissions(file_path)
    else:
        print(f"Error: {sudoers_d_path} directory not found.")

if __name__ == '__main__':
    process_sudoers_files()
