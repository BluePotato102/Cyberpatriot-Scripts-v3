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
        "/etc/security/limits.conf": "640",
        "/etc/crontab": "600",
        "/root/.ssh/authorized_keys": "600",
        "/etc/pam.conf": "640",
        "/etc/default/grub": "640",
        "/etc/grub.d/40_custom": "640",
        "/etc/pam.d/common-account": "640",
        "/etc/pam.d/common-password": "640"
    }
    
    for file, perm in files.items():
        if os.path.exists(file):
            current_perm = oct(stat.S_IMODE(os.lstat(file).st_mode))
            if current_perm != '0o' + perm:
                run_command(f"chmod {perm} {file}")


def run():
    check_permissions()
    #check_pam_permissions()
    #check_ownership_and_permissions()
    #find_world_writable()
    #add_security_permissions()

if __name__ == "__main__":
    run()
