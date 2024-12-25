import os
import subprocess

def remove_nullok_from_pam():
    """Remove all instances of 'nullok' from PAM configuration files."""
    print("Removing all instances of 'nullok' in /etc/pam.d...")
    pam_dir = "/etc/pam.d"
    for file_name in os.listdir(pam_dir):
        file_path = os.path.join(pam_dir, file_name)
        if os.path.isfile(file_path):
            subprocess.run(["sudo", "sed", "-i", "/nullok/d", file_path])
    print("Removed 'nullok' from all PAM configuration files.")

def configure_password_hashing():
    """Configure secure password hashing algorithm."""
    print("Configuring secure password hashing...")
    with open("/etc/login.defs", "a") as f:
        f.write("ENCRYPT_METHOD SHA512\n")
    subprocess.run(["sudo", "sed", "-i", 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS 90/', "/etc/login.defs"])
    print("Secure password hashing configured.")

def enforce_password_expiration():
    """Set password expiration policies: min age, max age, and warning period."""
    print("Enforcing password expiration policies...")
    with open("/etc/login.defs", "a") as f:
        f.write("PASS_MIN_DAYS 7\n")
        f.write("PASS_MAX_DAYS 90\n")
        f.write("PASS_WARN_AGE 14\n")
    print("Password expiration policies enforced.")

def enforce_min_password_length():
    """Enforce minimum password length."""
    print("Enforcing minimum password length...")
    with open("/etc/security/pwquality.conf", "a") as f:
        f.write("minlen = 12\n")
    print("Minimum password length enforced.")

def enforce_password_complexity():
    """Enable password complexity rules."""
    print("Enforcing password complexity rules...")
    with open("/etc/security/pwquality.conf", "a") as f:
        f.write("minclass = 3\n")
        f.write("retry = 3\n")
    print("Password complexity rules enforced.")

def remember_previous_passwords():
    """Configure the system to remember previous passwords."""
    print("Configuring previous password retention...")
    with open("/etc/pam.d/common-password", "a") as f:
        f.write("password requisite pam_unix.so remember=5\n")
    print("Retention of previous passwords configured.")

def enable_dictionary_checks():
    """Enable dictionary-based password strength checks."""
    print("Enabling dictionary-based password strength checks...")
    subprocess.run(["sudo", "apt-get", "install", "-y", "cracklib-runtime"])
    with open("/etc/pam.d/common-password", "a") as f:
        f.write("password requisite pam_pwquality.so retry=3\n")
    print("Dictionary-based password strength checks enabled.")

def main():
    """Master function to harden password policies."""
    print("Starting password hardening process...")
    remove_nullok_from_pam()
    configure_password_hashing()
    enforce_password_expiration()
    enforce_min_password_length()
    enforce_password_complexity()
    remember_previous_passwords()
    enable_dictionary_checks()
    print("Password hardening process completed.")

if __name__ == "__main__":
    main()
