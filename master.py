# master.py
import user_management
import guest_users
import password_hardening
import ssh_hardening
import file_permissions
import sysctl_hardening
import mediascript
import firewall
import package_audit
import secure_sudo

banner = """
  ____  ____     ___  __ __      __ __   ____  ______  _____
 /    ||    \   /  _]|  |  |    |  |  | /    ||      |/ ___/
|   __||  D  ) /  [_ |  |  |    |  |  ||  o  ||      (   \_ 
|  |  ||    / |    _]|  ~  |    |  _  ||     ||_|  |_|\__  |
|  |_ ||    \ |   [_ |___, |    |  |  ||  _  |  |  |  /  \ |
|     ||  .  \|     ||     |    |  |  ||  |  |  |  |  \    |
|___,_||__|\_||_____||____/     |__|__||__|__|  |__|   \___|
"""

print(banner)

def main():
    while True:
        print("\n=== Linux Hardening Menu ===")
        print("1. User Managment")
        print("2. Guest Users & Lockout")
        print("3. Password Length/Algorithm/Security")
        print("4. SSH Configuration")
        print("5. File Permissions Check/Secure")
        print("6. Sysctl Configuration")
        print("7. Media Management (Bash)")
        print("8. Firewall Setup")
        print("9. Package Audit")
        print("10. Secure Sudo")
        print("0. Exit")
        
        choice = input("Enter your choice (0-9): ")
        
        if choice == "1":
            user_management.run()
        elif choice == "2":
            guest_users.run()
        elif choice == "3":
            password_hardening.run()
        elif choice == "4":
            ssh_hardening.run()
        elif choice == "5":
            file_permissions.run()
        elif choice == "6":
            sysctl_hardening.run()
        elif choice == "7":
            mediascript.run()
        elif choice == "8":
            firewall.run()
        elif choice == "9":
            package_audit.run()
        elif choice == "10":
            secure_sudo.run()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
