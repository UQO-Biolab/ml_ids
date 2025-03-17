import os

def fusionner_fichiers(output_directory, single_json):
    """
    Fusionne tous les fichiers d'un répertoire dans un seul fichier de sortie.
    """
    with open(single_json, 'w', encoding='utf-8') as f_sortie:
        # List all files in the directory
        fichiers = os.listdir(output_directory)

        # Reading and writing the contents of each file to the output file
        for fichier in fichiers:
            chemin_fichier = os.path.join(output_directory, fichier)
            if os.path.isfile(chemin_fichier):
                try:
                    with open(chemin_fichier, 'r', encoding='utf-8') as f:
                        contenu = f.read()
                        f_sortie.write(contenu)
                        f_sortie.write('\n')  # Add a new line between file contents
                except Exception as e:
                    print(f"Erreur lors de la lecture du fichier {fichier} : {e}")
    print(f"Les fichiers ont été fusionnés dans {single_json}.")
