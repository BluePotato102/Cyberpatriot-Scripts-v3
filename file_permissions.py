import os
import stat

def run_command(command):
    """Executes a shell command."""
    os.system(command)

def file_permissions():
    """Sets specific permissions and ownership for critical files."""
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
            
            # Change the ownership to root:root
            print(f"Changing ownership of {file} to root:root")
            run_command(f"sudo chown root:root {file}")

def directory_permissions():
    """Sets appropriate permissions and ownership for critical directories, recursively."""
    directories = {
        "/etc/grub.d": "755",
        "/etc/pam.d": "755",
        "/etc/security": "755"
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
                
                # Change the ownership of the directory to root:root
                print(f"Changing ownership of {root} to root:root")
                run_command(f"sudo chown root:root {root}")
                
                # Set permissions for files inside the directory
                for file in files:
                    file_path = os.path.join(root, file)
                    current_file_perm = oct(stat.S_IMODE(os.lstat(file_path).st_mode))
                    if current_file_perm != f'0o{perm}':
                        print(f"Changing permissions of {file_path} from {current_file_perm} to {perm}")
                        run_command(f"chmod {perm} {file_path}")
                    
                    # Change the ownership of the file to root:root
                    print(f"Changing ownership of {file_path} to root:root")
                    run_command(f"sudo chown root:root {file_path}")

def run():
    """Runs the permission and ownership correction functions."""
    directory_permissions()
    file_permissions()

if __name__ == "__main__":
    run()
