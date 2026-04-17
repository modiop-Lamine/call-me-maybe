import argparse
import json
import sys
from llm_sdk.llm_sdk import Small_LLM_Model


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


# Initialize parser
parser = argparse.ArgumentParser(description="Tools for Function Calling with"
                                 " Qwen3-0.6B")

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

# Read the command in the terminal that launched the program
args = parser.parse_args()

# Load data
print("Loading files...")
functions_data = load_json_file(args.function_definition)
input_data = load_json_file(args.input)

print("Files succesfully loaded!")
print(f"-> {len(functions_data)} functions available.")
print(f"-> {len(input_data)} queries to process.")

# Loading the LLM
print("Loading Qwen3-0.6B in memory... (it may take some time)")
model = Small_LLM_Model()

for item in input_data:
    prompt = item.get("prompt")
    print(f"\nProcessing the query: '{prompt}'")

    # Turn the prompt in Input IDs
    input_ids = model.encode(prompt)

    print("The prompt has been changed in an Input ID:")
    print(input_ids)
