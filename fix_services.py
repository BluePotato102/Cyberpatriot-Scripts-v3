import subprocess
import os

def run_command(command):
    """Runs a system command and logs the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        return False

def disable_unnecessary_services():
    """Disables and stops unnecessary services."""
    print("Disabling unnecessary services...")
    services = [
        "bluetooth", "cups", "avahi-daemon", "rpcbind", "nfs-common", 
        "NetworkManager", "apache2", "mysql", "postfix", "smbd", "postfix"
    ]
    for service in services:
        run_command(f"sudo systemctl disable {service}")
        run_command(f"sudo systemctl stop {service}")

def enable_necessary_services():
    """Enables and starts necessary services."""
    print("Enabling necessary services...")
    services = [
        "apparmor", "rsyslog", "ufw", "ssh", "systemd-journald", 
        "cron", "systemd-timesyncd", "dbus"
    ]
    for service in services:
        run_command(f"sudo systemctl enable {service}")
        run_command(f"sudo systemctl start {service}")

def run():
    """Run the setup process for disabling unnecessary services and enabling necessary ones."""
    print("Starting system configuration...")
    disable_unnecessary_services()
    enable_necessary_services()
    print("System configuration completed.")

if __name__ == "__main__":
    run()
