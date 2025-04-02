import os 
from utils import load_json, compare_automata_json
from test_cases import regex_list
if __name__ == "__main__":
    # List of regex test cases

    # Generate folder names by replacing *, |, and ? with _
    folder_names = [regex.replace("*", "_").replace("|", "_").replace("?", "_") for regex in regex_list]

    # Base directories for test cases and output
    test_cases_dir = os.path.join(os.getcwd(), "test_cases")
    output_dir = os.path.join(os.getcwd(), "output")

    # Loop through each folder and compare JSONs
    for folder_name in folder_names:
        test_case_path = os.path.join(test_cases_dir, folder_name, "nfa.json")
        output_path = os.path.join(output_dir, folder_name, "nfa.json")

        if not os.path.exists(test_case_path):
            print(f"Test case JSON not found: {test_case_path}")
            continue

        if not os.path.exists(output_path):
            print(f"Output JSON not found: {output_path}")
            continue

        # Load and compare JSONs
        test_case_json = load_json(test_case_path)
        output_json = load_json(output_path)
        are_identical = compare_automata_json(test_case_json, output_json)

        # Print the result
        if are_identical:
            print(f"[NFA][PASS] Automata in folder '{folder_name}' are identical.")
        else:
            print(f"[NFA][FAIL] Automata in folder '{folder_name}' are NOT identical.")

    # Loop through each folder and compare JSONs
    for folder_name in folder_names:
        test_case_path = os.path.join(test_cases_dir, folder_name, "minimized_dfa.json")
        output_path = os.path.join(output_dir, folder_name, "minimized_dfa.json")

        if not os.path.exists(test_case_path):
            print(f"Test case JSON not found: {test_case_path}")
            continue

        if not os.path.exists(output_path):
            print(f"Output JSON not found: {output_path}")
            continue

        # Load and compare JSONs
        test_case_json = load_json(test_case_path)
        output_json = load_json(output_path)
        are_identical = compare_automata_json(test_case_json, output_json)

        # Print the result
        if are_identical:
            print(f"[DFA][PASS] Automata in folder '{folder_name}' are identical.")
        else:
            print(f"[DFA][FAIL] Automata in folder '{folder_name}' are NOT identical.")