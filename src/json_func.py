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


def write_json(new_data: dict, filename: str):
    # Create directory if they don't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Retrieve existing data or create an empty list
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                file_data = json.load(file)
            except json.JSONDecodeError:
                # If there is a problem with the file with reset data
                file_data = list()
    else:
        # If the file doesn't exist we start empty
        file_data = list()

    file_data.append(new_data)

    # Write in the file ('w' create the file if it doesn't exist)
    with open(filename, 'w') as file:
        json.dump(file_data, file, indent=4)
