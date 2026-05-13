import sys
import json
import os


def load_json_file(filepath: str):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"\033[91m[FileError] '{filepath}'\033[0m"
              "\n\t\x1b[38;5;244m# Couldn't be found\x1b[0m\n")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"\033[91m[JSONError] '{filepath}'\033[0m"
              "\n\t\x1b[38;5;244m# JSON is invalid\x1b[0m\n")
        sys.exit(1)
    except Exception as e:
        print(f"\033[91m[FileError] '{filepath}'\033[0m"
              f"\n\t\x1b[38;5;244m# {e}\x1b[0m\n")
        sys.exit(1)


def write_json(new_data, filename):
    # 1. Sécurité : Créer les dossiers parents s'ils n'existent pas
    # os.path.dirname récupère "data/output/", et makedirs le crée.
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # 2. Récupérer les données existantes OU créer une liste vide
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                file_data = json.load(file)
            except json.JSONDecodeError:
                # Si le fichier existe mais est vide ou mal formaté, on repart de zéro
                file_data = []
    else:
        # Si le fichier n'existe pas, on initialise une liste vide
        file_data = []

    # 3. Ajouter les nouvelles données
    # (J'ai remplacé file_data[0].append par file_data.append, qui est la norme 
    # pour ajouter un élément à une liste JSON principale)
    file_data.append(new_data)

    # 4. Écrire le tout dans le fichier (le mode 'w' crée le fichier s'il n'existe pas)
    with open(filename, 'w') as file:
        json.dump(file_data, file, indent=4)
