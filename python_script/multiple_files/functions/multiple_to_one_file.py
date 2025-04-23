import os
import glob

def merge_files(output_directory):
    patterns = ["attackers.json*", "ciscoasa.log*", "cowrie.json*", "dionaea.json*", "log.json*","log_session.json*","tanner_report.json*","honeyaml.log*"]

    for pattern in patterns:
        # Use glob to get all files matching the pattern
        files = glob.glob(os.path.join(output_directory, pattern))

        # Determine output file name based on pattern
        single_json = os.path.join(output_directory, f"fusion_{pattern.split('.')[0]}.json")

        with open(single_json, 'w', encoding='utf-8') as f_output:
            # Read and write the contents of each file to the output file
            for file in files:
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        contenu = f.read()
                        f_output.write(contenu)
                        f_output.write('\n')
                except Exception as e:
                    print(f"Error reading file {file} : {e}")
        print(f"Files matching pattern '{pattern}' have been merged into {single_json}.")

