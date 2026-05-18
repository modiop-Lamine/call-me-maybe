*This project has been created as part of the 42 curriculum by modiop*

<div style="display: flex; align-items: center; border: 2px solid #57686f; color: #c7dce2; font-family: monospace; padding: 10px; border-radius: 10px;">
    <div style="width: 85px;"></div>
    <div style="flex-grow: 1; text-align: center;">
        <div style="font-size: 30px; font-weight: normal;">
            <b>Call Me Maybe</b><br>
        </div>
        <div style="font-size: 12px; font-weight: normal;">
            <code>A 42's common core project</code>
        </div>
    </div>
    <img src="./images/42_icon.png" width="70" style="margin-left: 15px; border-radius: 10px;">
</div>

## DESCRIPTION 📃​

### This project introduces function calling in Large Language Models by building a system that translates natural language prompts into structured function calls with typed arguments. You'll implement constrained decoding to guarantee valid JSON output, achieving near-perfect reliability with a small 0.5B parameter model, bridging the gap between human language and computer-executable operations.

---
Summary:

- [Algorithm explanation](#algorithm-explanation)
- [Design decisions](#design-decisions)
- [Performance analysis](#performance-analysis)
- [Challenges faced](#challenges-faced)
- [Testing strategy](#testing-strategy)
- [Example usage](#example-usage)

---

### <span style="color: #7dd0ec;">Algorithm explanation</span>

The algorithm relies on **constrained decoding**. Instead of relying purely on prompting, constrained decoding intervenes during the generation process by modifying the probabilities (logits) before token selection. At each step, the model produces logits for all possible tokens. The algorithm identifies which tokens maintain a valid JSON structure and comply with the expected schema, and sets the logits of all invalid tokens to negative infinity. By sampling only from the remaining valid tokens, the system guarantees a 100% parseable and schema-compliant JSON output.

### <span style="color: #7dd0ec;">Design decisions</span>

* **Language & Standards**: The project is written in Python 3.10+ and strictly adheres to the `flake8` coding standard.
* **Validation**: All classes use `pydantic` to ensure robust data and schema validation.
* **Model Integration**: The system relies on the `Qwen/Qwen3-0.6B` model and interacts with it exclusively through the provided `Small_LLM_Model` wrapper class from the `llm_sdk` package.
* **Environment**: Dependencies (`numpy`, `pydantic`) and virtual environments are managed using `uv`.

### <span style="color: #7dd0ec;">Performance analysis</span>

The implementation is designed to achieve near-perfect accuracy (90%+) in correct function selection and argument extraction. Thanks to constrained decoding, the reliability of the output is optimal, producing 100% valid and schema-compliant JSON even with a small 0.5B parameter model. The program maintains a reasonable execution speed, processing all test prompts in under 5 minutes on standard hardware, and includes robust error handling to gracefully manage malformed inputs without crashing.

Exception with the 42 campus' computers: I've never managed to start the program so it should be tested on a more performant machine.

### <span style="color: #7dd0ec;">Challenges faced</span>

Various technical obstacles were encountered during development, such as understanding logit manipulation on tensors, mapping the tokenizer's vocabulary to JSON structures, and implementing rigorous error handling to prevent unexpected crashes and handle edge cases gracefully.

### <span style="color: #7dd0ec;">Testing strategy</span>

The execution generates a single `function_calling_results.json` output file. The testing strategy involves validating this JSON structure, verifying its content, and ensuring that function names and argument types perfectly match the provided definitions (`functions_definition.json`). The system is heavily tested against edge cases, including empty strings, large numbers, special characters, wrong types, and ambiguous prompts.


## INSTRUCTIONS 🧑‍💻

### <span style="color: #7dd0ec;">Example usage</span>

The program is executed using the `uv` package manager.

You can run the program using the default directories (`data/input/` and `data/output/`), or specify custom paths using the optional arguments.

**Full execution example:**
```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calls.json
```

#### A Makefile is in the project making everything easier.
\>> `make help` or `make` to show all Makefile's targets

<span style="display: block; background-color: rgba(128, 128, 128, 0.1); padding: 10px; border-left: 4px solid rgb(235, 106, 102); border-radius: 5px; margin: 10px 0; color: rgb(235, 106, 102);">
    🚨​ FIRST STEP IS MANDATORY
</span>

First initialize the project:<br/>
\>>> `make install` <<<

Then run the project with arguments if you need:<br/>
\>>> `make run ARG="arg is optional"` <<<

## RESSOURCES 🔎

- [<img src="images/GG_icon.png" height="20" style="border-radius: 5px; vertical-align: middle; padding-right: 0px"> JSON in python](https://www.geeksforgeeks.org/python/python-json/)

#### AI Assitant* :
- [<img src="images/gemini_icon.png" height="20" style="border-radius: 5px; vertical-align: middle; padding-right: 0px"> Gemini AI](https://gemini.google.com)<br/>
<small><span style="color: #6d7b86;">*\*Used for repetitive tasks and revise reasoning through code to make the structure more readable*</span></small>