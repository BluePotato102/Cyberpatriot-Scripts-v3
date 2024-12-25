import os
import stat

def run_command(command):
    """Executes a shell command."""
    os.system(command)

def file_permissions():
    """Sets specific permissions for critical files."""
    files = {
        "/etc/passwd": "644",
        "/etc/shadow": "600",
        "/etc/group": "644",
        "/etc/gshadow": "600",
        "/etc/ssh/sshd_config": "600",
        "/etc/security/access.conf": "600",
        "/etc/security/limits.conf": "640",
        "/etc/crontab": "600",
        "/root/.ssh/authorized_keys": "600",
        "/etc/pam.conf": "640",
        "/etc/default/grub": "640"
    }
    
    for file, perm in files.items():
        if os.path.exists(file):
            # Get the current permissions of the file
            current_perm = oct(stat.S_IMODE(os.lstat(file).st_mode))
            
            # Compare with the desired permission and update if necessary
            if current_perm != f'0o{perm}':
                print(f"Changing permissions of {file} from {current_perm} to {perm}")
                run_command(f"chmod {perm} {file}")

def directory_permissions():
    """Sets appropriate permissions for critical directories, recursively."""
    directories = {
        "/etc/grub.d": "755",
        "/etc/pam.d": "755",
        "/etc/security": "750"
    }

    for directory, perm in directories.items():
        if os.path.exists(directory):
            # Walk through the directory and set permissions for files and subdirectories
            for root, dirs, files in os.walk(directory):
                # Set directory permissions
                current_dir_perm = oct(stat.S_IMODE(os.lstat(root).st_mode))
                if current_dir_perm != f'0o{perm}':
                    print(f"Changing permissions of {root} from {current_dir_perm} to {perm}")
                    run_command(f"chmod {perm} {root}")
                else:
                    print(f"Permissions for {root} are already correct.")
                
                # Set permissions for files inside the directory
                for file in files:
                    file_path = os.path.join(root, file)
                    current_file_perm = oct(stat.S_IMODE(os.lstat(file_path).st_mode))
                    if current_file_perm != f'0o{perm}':
                        print(f"Changing permissions of {file_path} from {current_file_perm} to {perm}")
                        run_command(f"chmod {perm} {file_path}")


def run():
    """Runs the permission correction functions."""
    file_permissions()
    directory_permissions()

if __name__ == "__main__":
    run()
