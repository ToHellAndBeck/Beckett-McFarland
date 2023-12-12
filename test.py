import subprocess

# Example command: "ls" to list files in the current directory
command = "fortune | lolcat"

# Run the command and capture its output
result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)

# Check if the command was successful
if result.returncode == 0:
    # Print the output
    print("Command output:")
    print(result.stdout)
else:
    # Print an error message
    print(f"Error: Command exited with code {result.returncode}")
