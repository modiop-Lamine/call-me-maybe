import argparse
import json
import sys
import os
import numpy as np
from llm_sdk.llm_sdk import Small_LLM_Model
from pydantic import BaseModel
from typing import Any, Dict


class FunctionCallOutput(BaseModel):
    prompt: str
    name: str
    parameters: Dict[str, Any]


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


def build_system_prompt(user_query: str, functions_list: list) -> str:
    functions_str = json.dumps(functions_list, indent=2)

    system_prompt = f"""You are a smart AI that translates human requests into structured function calls.
Here is the list of available functions you can use, along with their descriptions and parameters:

{functions_str}

The user's request is: "{user_query}"

You must respond ONLY with a JSON object. Do not add any explanation.
The JSON object must contain exactly these three keys:
- "prompt": the exact user request.
- "name": the exact name of the function chosen from the list above.
- "parameters": an object containing the required arguments.

JSON Output:
    """

    return system_prompt


def initialize_parser():
    parser = argparse.ArgumentParser(description="Tools for Function Calling "
                                     "with Qwen3-0.6B")

    parser.add_argument(
        "--function-definition",
        type=str,
        default="data/input/function_definitions.json",
        help="Path to the file with function definitions"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/input/function_calling_tests.json",
        help="Path to the file with test queries"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calling_results.json",
        help="Path to the output file for the results"
    )

    return parser


def write_json(new_data, filename='data/output/function_calling_results.json'):
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


def generate_function_call():
    for item in input_data:
        user_query = item.get("prompt")
        print("\n======================================")
        print(f"\nProcessing the query: '{user_query}'")

        # We build a big text of instructions
        full_prompt = build_system_prompt(user_query, functions_data)

        # Turn the prompt in Input IDs and turn it from Tensor to list
        input_ids = model.encode(full_prompt)[0].tolist()

        # Prepare a storage for the answer and put a limit of tokens
        generated_tokens = []
        generated_text = ""
        max_tokens = 50

        # The strings we want the LLM to write
        valid_paths = []
        for func in functions_data:
            func_name = func["name"]
            # On force l'IA à écrire le prompt, le nom exact, et à ouvrir les paramètres
            path = f'{{"prompt": "{user_query}", "name": "{func_name}", "parameters": {{'
            valid_paths.append(path)

        print("Generating answer...")

        while len(generated_tokens) < max_tokens:

            logits = model.get_logits_from_input_ids(input_ids)
            logits_array = np.array(logits)

            # We set all token probability to negtive inf by default
            mask = np.full(logits_array.shape, -np.inf)

            for token_id, token_str in id_to_token.items():
                # We replace the 'Ġ' used by default to ' ' for this test
                clean_token_str = token_str.replace("Ġ", " ")

                # What the answer should look like
                potential_text = generated_text + clean_token_str

                is_valid_token = False
                # We check if the token is one of the path
                for path in valid_paths:
                    if path.startswith(potential_text) or potential_text.startswith(path):
                        is_valid_token = True
                        break

                if is_valid_token:
                    mask[token_id] = logits_array[token_id]

            logits_array = mask

            # We apply our mask
            logits_array = mask

            # Take the token with the highest probability
            next_token_id = int(np.argmax(logits_array))

            generated_tokens.append(next_token_id)
            input_ids.append(next_token_id)

            new_text_piece = model.decode([next_token_id])
            generated_text += new_text_piece

            if generated_text.count("{") > 0 and generated_text.count("{") == generated_text.count("}"):
                print("\n>>> JSON fully generated.")
                break

        try:
            json_dict = json.loads(generated_text)
            final_output = FunctionCallOutput(**json_dict)
            print("\nPydantic validation successful.")
            write_json(final_output.model_dump())
        except Exception as e:
            print("\nValidation Error:", e)


# Initialize parser
parser = initialize_parser()

# Read the options of the command in the terminal that launched the program
args = parser.parse_args()

# Load data
print("Loading files...")
functions_data = load_json_file(args.function_definition)
input_data = load_json_file(args.input)

print("Files succesfully loaded!")
print(f"-> {len(functions_data)} functions available.")
print(f"-> {len(input_data)} queries to process.\n")

# Loading the LLM
print("Loading Qwen3-0.6B in memory... (it may take some time)")
model = Small_LLM_Model()

# Load vocabulary of the model
with open(model.get_path_to_vocab_file(), 'r') as f:
    vocab = json.load(f)

# Reverse the keys and value to search the dict by token
id_to_token = {v: k for k, v in vocab.items()}
print(f"Vocabulary loaded : {len(vocab)} tokens availables.")

# Retrieve the ID of the open bracket "{"
id_open_bracket = model.encode("{")[0].tolist()
print(id_open_bracket)

generate_function_call()
