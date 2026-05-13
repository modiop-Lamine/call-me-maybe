import json
from llm_sdk.llm_sdk import Small_LLM_Model
from json_func import load_json_file
from parser import initialize_parser
from llm_func import generate_function_call


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

generate_function_call(functions_data, input_data, args, model, id_to_token)
