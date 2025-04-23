import os
import glob

def delete_unused_files(output_directory):
    # Delete file attacker.log.* / honeytrap.log.* / dionaea.sqlite.*
    pattern_to_delete = ["attacker.log*", "honeytrap.log*", "dionaea.sqlite*"]
    for pattern in pattern_to_delete:
        # Using glob to get the list of files matching the pattern
        files = glob.glob(os.path.join(output_directory, pattern))

        # Delete each file matching the pattern
        for file in files:
            try:
                os.remove(file)
                print(f"The file {file} was successfully deleted.")            
            except FileNotFoundError:
                print(f"The file {file} does not exist.")
            except PermissionError:
                print(f"You do not have the necessary permissions to delete the file {file}.")
            except Exception as e:
                print(f"An error occurred: {e}")