import json

def tester_fichier_json(single_json_filtered):
    try:
        with open(single_json_filtered, 'r', encoding='utf-8') as fichier:
            # Try to parse the file contents as JSON
            contenu = json.load(fichier)
            print(f"Le fichier {single_json_filtered} est un JSON valide.")
            return contenu
    except json.JSONDecodeError as e:
        print(f"Erreur JSON dans le fichier {single_json_filtered} : {e}")
    except FileNotFoundError:
        print(f"Le fichier {single_json_filtered} n'existe pas.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du fichier {single_json_filtered} : {e}")
