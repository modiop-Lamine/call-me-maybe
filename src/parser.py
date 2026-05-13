import argparse


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
