import os
import subprocess

def run_command(command):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr.strip()} for command: {command}")
        return result.stdout.strip()
    except Exception as e:
        print(f"Exception occurred while running command: {command}\n{e}")

# Enforce screen timeout policy
run_command("sudo -u ratman gsettings set org.gnome.desktop.session idle-delay 300")

# Enable automatic screen lock
run_command("sudo -u ratman gsettings set org.gnome.desktop.screensaver lock-enabled true")

# Ensure automatic updates are enabled
run_command("sudo apt install unattended-upgrades -y")

# Add user caroline and configure SSH key permissions
run_command("sudo useradd -m caroline")
run_command("sudo usermod -aG aperturestaff caroline")
os.makedirs("/home/caroline/.ssh", exist_ok=True)
os.chmod("/home/caroline/.ssh", 0o700)

# Add cjohnson as an administrator
run_command("sudo useradd -m cjohnson")
run_command("sudo usermod -aG sudo,adm cjohnson")

# Add chell to testsubjects group
run_command("sudo useradd -m chell")
run_command("sudo usermod -aG testsubjects chell")

# Disable automatic login for ratman
run_command("sudo sed -i 's/^AutomaticLoginEnable=true/AutomaticLoginEnable=false/' /etc/gdm3/custom.conf")

# Remove unauthorized user wheatley
run_command("sudo userdel -r wheatley")

# Secure password for companioncube
secure_password = "$y$j9T$KSdv3iaCthqz.nxfJU5/f1$3BlSl4dvR3r1le/bDhYpPfjMb14z/K5.ZdXLLa0JO23"
run_command(f"echo 'companioncube:{secure_password}' | sudo chpasswd -e")

# Lock root account
run_command("sudo passwd -l root")

# Remove prohibited MP3 files
run_command("sudo rm -f /home/cjohnson/Music/radio.mp3")
run_command("sudo rm -f /home/spacecore/Music/spaaaaaace.mp3")

# Enable and configure UFW firewall
run_command("sudo ufw default deny incoming")
run_command("sudo ufw default allow outgoing")
run_command("sudo ufw enable")
run_command("sudo ufw allow 22")

# Disable NFS services
nfs_services = ["nfs-blkmap", "nfs-idmapd", "nfs-mountd", "nfsdcld", "nfs-server", "nfs-kernel-server"]
for service in nfs_services:
    run_command(f"sudo systemctl stop {service}")
    run_command(f"sudo systemctl disable {service}")

# Ensure Apache is running and configured securely
run_command("sudo systemctl enable apache2")
run_command("sudo systemctl start apache2")
run_command("sudo sed -i 's/^ServerTokens.*/ServerTokens Prod/' /etc/apache2/conf-enabled/security.conf")
run_command("sudo sed -i 's/^ServerSignature.*/ServerSignature Off/' /etc/apache2/conf-enabled/security.conf")

# Secure SSH configuration
run_command("sudo sed -i 's/^#?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config")
run_command("sudo sed -i 's/^#?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config")
run_command("sudo sed -i 's/^#?Port.*/Port 1382/' /etc/ssh/sshd_config")
run_command("sudo systemctl restart ssh")

# Enforce password complexity
password_settings = {
    "minlen": 8,
    "ucredit": -1,
    "lcredit": -1,
    "ocredit": -1,
    "dcredit": -1,
    "dictcheck": 1,
    "usercheck": 1
}
with open("/etc/security/pwquality.conf", "w") as pw_file:
    for key, value in password_settings.items():
        pw_file.write(f"{key} = {value}\n")

# Set secure sysctl parameters
sysctl_settings = {
    "net.ipv4.tcp_rfc1337": 1,
    "net.ipv4.tcp_syncookies": 1,
    "net.ipv4.ip_forward": 0,
    "net.ipv4.conf.all.accept_source_route": 0,
    "net.ipv4.conf.default.accept_source_route": 0,
    "net.ipv4.conf.all.send_redirects": 0,
    "net.ipv4.conf.default.send_redirects": 0,
    "net.ipv4.conf.all.log_martians": 1
}
with open("/etc/sysctl.conf", "a") as sysctl_file:
    for key, value in sysctl_settings.items():
        sysctl_file.write(f"{key} = {value}\n")
run_command("sudo sysctl -p")

# Ensure AppArmor is running
run_command("sudo systemctl enable apparmor")
run_command("sudo systemctl start apparmor")

print("All security configurations have been enforced aggressively!")
