# Lexical Analyzer

This project implements a lexical analyzer that processes regular expressions to generate and visualize their corresponding NFA, DFA, and minimized DFA representations. It also provides functionality to save these representations in JSON format for further analysis.

## Project Structure

- **`nfa.py`**: Contains the implementation of the NFA (Non-deterministic Finite Automaton) and related utilities.
- **`dfa.py`**: Contains the implementation of the DFA (Deterministic Finite Automaton) and related utilities.
- **`minimized_dfa.py`**: Contains the implementation of the Minimized DFA and related utilities.
- **`regex_preprocessor.py`**: Handles preprocessing of regular expressions.
- **`generate_test_cases.py`**: Automates the generation of NFA, DFA, and Minimized DFA for a list of regular expressions and saves their visualizations and JSON representations.
- **`run_test_cases.py`**: Executes test cases to validate the correctness of the lexical analyzer.
- **`test_cases.py`**: Contains a list of regular expressions used as test cases.
- **`output/`**: Stores the generated visualizations (`.png`) and JSON files for each test case.

## How to Use

1. **Generate Test Cases**:
   - Run `generate_test_cases.py` to process the regular expressions in `test_cases.py`.
   - The output will be saved in the `output/` directory, organized by folder names derived from the regular expressions.

2. **Run Test Cases**:
   - Use `run_test_cases.py` to validate the generated automata against predefined test cases.

3. **Visualizations**:
   - Visual representations of the NFA, DFA, and Minimized DFA are saved as `.png` files in the respective output folders.

## Dependencies

- Python 3.x
- Libraries:
  - `os`
  - `json`
  - Any additional libraries required for graph plotting (e.g., `matplotlib`, `graphviz`).

## Example

To generate automata for the test cases:
```bash
python generate_test_cases.py
```

To run the test cases:
```bash
python run_test_cases.py
```

## Output Structure

The `output/` directory contains subfolders for each regular expression. Each subfolder includes:
- `nfa.png`: Visualization of the NFA.
- `nfa.json`: JSON representation of the NFA.
- `dfa.png`: Visualization of the DFA.
- `dfa.json`: JSON representation of the DFA.
- `minimized_dfa.png`: Visualization of the Minimized DFA.
- `minimized_dfa.json`: JSON representation of the Minimized DFA.

## Contribution

Feel free to contribute by adding more test cases or improving the automata generation algorithms. Ensure that all changes are tested using the provided framework.

## License

This project is for educational purposes and is licensed under [MIT License](LICENSE).