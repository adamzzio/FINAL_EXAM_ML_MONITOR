import subprocess

# Add the modified file to the staging area
subprocess.call(["git", "add", "iris_model.sav"])

# Commit the changes with a message
subprocess.call(["git", "commit", "-m", "Add trained iris model"])

# Push the changes to the remote repository
subprocess.call(["git", "push", "origin", "main"])
