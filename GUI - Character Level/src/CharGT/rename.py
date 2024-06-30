import os

# Set the path to the directory containing the files
path = './'

# Loop through each file in the directory
for filename in os.listdir(path):
    if filename.endswith(".gt.txt"):
        # Generate the new filename by replacing '.gt.txt' with '.txt'
        new_filename = filename.replace(".gt.txt", ".txt")
        # Generate the full paths
        old_file = os.path.join(path, filename)
        new_file = os.path.join(path, new_filename)
        # Rename the file
        os.rename(old_file, new_file)
        print(f"Renamed '{filename}' to '{new_filename}'")

print("All files have been renamed.")
