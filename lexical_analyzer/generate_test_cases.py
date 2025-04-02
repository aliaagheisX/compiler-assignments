import os
import json
from nfa import NFA, plot_nfa, save_nfa_to_json
from dfa import DFA, plot_dfa,save_dfa_to_json
from minimized_dfa import MinimizedDFA, plot_minimized_dfa, save_minimized_dfa_to_json
from test_cases import regex_list

if __name__ == "__main__":

    # Generate folder names by replacing *, |, and ? with _
    folder_names = [regex.replace("*", "_").replace("|", "_").replace("?", "_") for regex in regex_list]

    for regex, folder_name in zip(regex_list, folder_names):
        # Create output folder for each regex
        output_folder = os.path.join(os.getcwd(), "output", folder_name)
        os.makedirs(output_folder, exist_ok=True)

        nfa = NFA().build_nfa_from_postfix(regex)
        dfa = DFA(nfa)
        minimized_dfa = MinimizedDFA(dfa)

        plot_nfa(nfa, "nfa.png", output_folder)
        save_nfa_to_json(nfa, "nfa.json", output_folder)

        plot_dfa(dfa, "dfa.png", output_folder)
        save_dfa_to_json(dfa, "dfa.json", output_folder)

        plot_minimized_dfa(minimized_dfa,  output_folder)
        save_minimized_dfa_to_json(minimized_dfa, "minimized_dfa.json", output_folder)
