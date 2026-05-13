import json
import numpy as np
from typing import Any
from argparse import Namespace
from llm_sdk.llm_sdk import Small_LLM_Model
from json_func import write_json
from FunctionCallOutput import FunctionCallOutput


def build_system_prompt(user_query: str, functions_list: list) -> str:
    functions_str = json.dumps(functions_list, indent=2)

    system_prompt = "You are a smart AI that translates human requests into "
    "structured function calls.\n"
    "Here is the list of available functions you can use, along with their "
    "descriptions and parameters:\n\n"
    f"{functions_str}\n\n"
    f"The user's request is: \"{user_query}\"\n\n"
    "If none of the functions match the user's request, use the function name "
    "\"fn_not_found\".\n\n"
    "You must respond ONLY with a JSON object. Do not add any explanation.\n"
    "The JSON object must contain exactly these three keys:\n"
    "- \"prompt\": the exact user request.\n"
    "- \"name\": the exact name of the function chosen from the list above (or"
    "\"fn_not_found\").\n"
    "- \"parameters\": an object containing the required arguments (can be "
    "empty if not found).\n\n"
    "JSON Output:"

    return system_prompt


def generate_function_call(
        functions_data: Any, input_data: Any, args: Namespace,
        model: Small_LLM_Model, id_to_token: dict
):
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
            # We make sure the IA build the text correctly
            path = f'{{"prompt": "{user_query}", "name": "{func_name}", '
            '"parameters": {{'
            valid_paths.append(path)

        error_path = f'{{"prompt": "{user_query}", "name": "fn_not_found", '
        '"parameters": {{'
        valid_paths.append(error_path)

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
                    if (
                        path.startswith(potential_text)
                        or potential_text.startswith(path)
                    ):
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

            if (
                generated_text.count("{") > 0
                and generated_text.count("{") == generated_text.count("}")
            ):
                print("\n>>> JSON fully generated.")
                break

        try:
            json_dict = json.loads(generated_text)
            final_output = FunctionCallOutput(**json_dict)
            print("\nPydantic validation successful.")
            if final_output.name == "fn_not_found":
                print("\n\033[91m[Error]: No function match the prompt: "
                      f"'{user_query}'\033[0m")
            write_json(final_output.model_dump(), args.output)
        except Exception as e:
            print(f"\n\033[91mValidation Error: {e}\033[0m")
