import os
import glob

def delete_unused_files(output_directory):
    # Delete file attacker.log.* / honeytrap.log.* / dionaea.sqlite.*
    pattern_to_delete = ["attacker.log*", "honeytrap.log*", "dionaea.sqlite*"]
    for pattern in pattern_to_delete:
        # Using glob to get the list of files matching the pattern
        fichiers = glob.glob(os.path.join(output_directory, pattern))

        # Delete each file matching the pattern
        for fichier in fichiers:
            try:
                os.remove(fichier)
                print(f"Le fichier {fichier} a été supprimé avec succès.")
            except FileNotFoundError:
                print(f"Le fichier {fichier} n'existe pas.")
            except PermissionError:
                print(f"Vous n'avez pas les permissions nécessaires pour supprimer le fichier {fichier}.")
            except Exception as e:
                print(f"Une erreur s'est produite : {e}")
