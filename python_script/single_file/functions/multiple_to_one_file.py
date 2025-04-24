import os

def merge_files(output_directory, single_json):
    with open(single_json, 'w', encoding='utf-8') as f_sortie:
        # List all files in the directory
        files = os.listdir(output_directory)

        # Reading and writing the contents of each file to the output file
        for file in files:
            chemin_fichier = os.path.join(output_directory, file)
            if os.path.isfile(chemin_fichier):
                try:
                    with open(chemin_fichier, 'r', encoding='utf-8') as f:
                        contenu = f.read()
                        f_sortie.write(contenu)
                        f_sortie.write('\n')
                except Exception as e:
                    print(f"Error reading file {file} : {e}")
    print(f"The files have been merged into {single_json}.")