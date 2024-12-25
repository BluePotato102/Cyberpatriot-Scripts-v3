import subprocess

def run():
    # Define the find command with all the options and file types
    find_command = [
        "find", "/home", "-type", "f", 
        "(",
        "-iname", "*.mp3", "-o",
        "-iname", "*.wav", "-o",
        "-iname", "*.mp4", "-o",
        "-iname", "*.mkv", "-o",
        "-iname", "*.jpg", "-o",
        "-iname", "*.jpeg", "-o",
        "-iname", "*.png", "-o",
        "-iname", "*.gif", "-o",
        "-iname", "*.webp", 
        ")",
        "-not", "-path", "*/.*"
    ]
    
    # Run the command using subprocess.run() and capture the output
    result = subprocess.run(find_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode == 0:
        # Print the output if the command is successful
        print(result.stdout)
    else:
        # Print the error if the command fails
        print("Error:", result.stderr)

if __name__ == "__main__":
    run()
