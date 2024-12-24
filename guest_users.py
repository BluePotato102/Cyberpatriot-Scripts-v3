import os
import subprocess

def modify_common_auth():
    file_path = "/etc/pam.d/common-auth"
    temp_file_path = file_path + ".tmp"
    required_line = "auth    required                        pam_tally2.so deny=5 unlock_time=300 onerr=fail\n"

    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

        if required_line not in lines:
            lines.insert(0, required_line)

        for i, line in enumerate(lines):
            if "pam_tally2.so" in line and "deny=" not in line:
                lines[i] = line.strip() + " deny=5 unlock_time=1800 onerr=fail\n"

        with open(temp_file_path, "w") as f:
            f.writelines(lines)

        os.replace(temp_file_path, file_path)
        print(f"Modified {file_path} successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def disable_guest_users():
    print("Disabling guest users...")
    display_managers = {
        "lightdm": "/etc/lightdm/lightdm.conf",
        "gdm": "/etc/gdm3/custom.conf",
        "sddm": "/etc/sddm.conf"
    }

    try:
        for dm, config_file in display_managers.items():
            status = subprocess.run(["sudo", "systemctl", "is-active", dm], capture_output=True, text=True)
            if status.stdout.strip() == "active":
                if dm == "lightdm":
                    subprocess.run(["sudo", "sh", "-c", f"echo '[SeatDefaults]' >> {config_file}"])
                    subprocess.run(["sudo", "sh", "-c", f"echo 'allow-guest=false' >> {config_file}"])
                    print("Guest user login disabled in LightDM.")
                elif dm == "gdm":
                    subprocess.run(["sudo", "sh", "-c", f"echo -e '\\n[security]\\nAllowGuest=false' >> {config_file}"])
                    print("Guest user login disabled in GDM.")
                elif dm == "sddm":
                    subprocess.run(["sudo", "sh", "-c", f"echo -e '[General]\\nEnableGuest=false' >> {config_file}"])
                    print("Guest user login disabled in SDDM.")
                break
        else:
            print("No supported display manager is currently active. Please manually configure guest login settings.")
    except Exception as e:
        print(f"An error occurred while disabling guest users: {e}")

if __name__ == "__main__":
    modify_common_auth()
    disable_guest_users()
