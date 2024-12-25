import subprocess

# Function to run a system command
def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        raise

# Main function to configure the firewall
def configure_firewall():
    # Enable UFW (Uncomplicated Firewall)
    run_command("sudo ufw enable")
    
    # Set default policy: deny incoming, allow outgoing
    run_command("sudo ufw default deny incoming")
    run_command("sudo ufw default allow outgoing")
    
    # Allow SSH, HTTP, and HTTPS traffic
    run_command("sudo ufw allow ssh")
    run_command("sudo ufw allow http")
    run_command("sudo ufw allow https")


def run():
    configure_firewall()

# Run the configuration
if __name__ == "__main__":
    run()
