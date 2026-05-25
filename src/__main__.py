import os
import sys

missing = list()

if os.path.exists('data/input/function_calling_tests.json') is False:
    missing.append('data/input/function_calling_tests.json')

if os.path.exists('data/input/functions_definition.json') is False:
    missing.append('data/input/functions_definition.json')

if os.path.isdir('data/input') is False:
    missing.append('data/input/')

if os.path.isdir('data') is False:
    missing.append('data/')

try:
    from src import llm_func
except ModuleNotFoundError:
    if os.path.isdir('llm_sdk/llm_sdk') is False:
        missing.append('llm_sdk/llm_sdk/')

    if os.path.isdir('llm_sdk') is False:
        missing.append('llm_sdk/')

if missing:
    missing.reverse()

    print("[MissingFilesError] The following files are missing to start "
          "the program:")
    for path in missing:
        print(f"- {path}")

    sys.exit(1)

llm_func.main()
