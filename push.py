import subprocess

# Ask the user for the commit message
commit_message = input("Enter your commit message: ")

# Run Git commands
try:
    # git add .
    subprocess.run(["git", "add", "."], check=True)
    
    # git commit -m "message"
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    
    # git push
    subprocess.run(["git", "push"], check=True)
    
    print("Changes pushed successfully!")
except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")
