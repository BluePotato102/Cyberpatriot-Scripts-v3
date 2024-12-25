import os
import stat

def run_command(command):
    """Executes a shell command."""
    os.system(command)

def check_permissions():
    files = {
        "/etc/passwd": "644",
        "/etc/shadow": "600",
        "/etc/group": "644",
        "/etc/gshadow": "600",
        "/etc/ssh/sshd_config": "600",
        "/etc/security/access.conf": "600",
        "/etc/security/limits.conf": "644",
        "/etc/crontab": "600",
        "/root/.ssh/authorized_keys": "600",
        "/etc/pam.conf": "644",
        "/etc/default/grub": "644",  # Added GRUB file for checking
    }
    
    for file, perm in files.items():
        if os.path.exists(file):
            current_perm = oct(stat.S_IMODE(os.lstat(file).st_mode))
            if current_perm != '0o' + perm:
                run_command(f"chmod {perm} {file}")

def check_pam_permissions():
    pam_dir = "/etc/pam.d/"
    
    # Ensure the /etc/pam.d directory has correct ownership and permissions
    if os.path.exists(pam_dir):
        run_command(f"chown -R root:root {pam_dir}")
        run_command(f"chmod -R 755 {pam_dir}")
    
    pam_files = [
        "/etc/pam.conf",
        "/etc/pam.d/common-auth",
        "/etc/pam.d/common-account",
        "/etc/pam.d/common-password",
        "/etc/pam.d/common-session",
    ]
    
    for file in pam_files:
        if os.path.exists(file):
            run_command(f"chmod 644 {file}")
            run_command(f"chown root:root {file}")

def check_ownership_and_permissions():
    dirs = {
        "/etc": "root:root",
        "/boot": "root:root",
        "/root": "root:root",
        "/var/log": "root:root",
        "/var/spool/cron": "root:root",
        "/var/tmp": "root:root",  # /tmp is typically world-writable, but /var/tmp should be restricted
        "/usr/local/bin": "root:root",
    }

    for dir, owner in dirs.items():
        if os.path.exists(dir):
            run_command(f"chown -R {owner} {dir}")
            run_command(f"find {dir} -type f -exec chmod 644 {{}} \;")
            run_command(f"find {dir} -type d -exec chmod 755 {{}} \;")

            # Check for world-writable files and directories
            run_command(f"find {dir} -type f -perm 0777 -exec ls -ld {{}} \;")
            run_command(f"find {dir} -type d -perm 0777 -exec ls -ld {{}} \;")

def find_world_writable():
    # Check the entire filesystem for world-writable files and directories
    run_command("find / -perm 0777 -type f -exec ls -ld {} \\;")
    run_command("find / -perm 0777 -type d -exec ls -ld {} \\;")

def add_security_permissions():
    # Ensure critical directories have secure permissions (e.g., /etc, /var)
    critical_dirs = [
        "/etc", "/boot", "/var", "/root", "/usr/local", "/home", "/lib"
    ]
    for dir in critical_dirs:
        if os.path.exists(dir):
            run_command(f"chmod 755 {dir}")
            run_command(f"chown root:root {dir}")

def run():
    check_permissions()
    #check_pam_permissions()
    #check_ownership_and_permissions()
    #find_world_writable()
    #add_security_permissions()

if __name__ == "__main__":
    run()
