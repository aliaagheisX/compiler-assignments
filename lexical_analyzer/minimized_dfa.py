import os
import json
from nfa import NFA, plot_nfa, save_nfa_to_json
from dfa import DFA, plot_dfa,save_dfa_to_json
from utils import plot_fsm
from test_cases import regex_list

class MinimizedDFA:
    def __init__(self, dfa):
        """
        Initialize the MinimizedDFA with a given DFA.
        """
        self.dfa = dfa
        self.minimized_transitions = {}
        self.start_state = None
        self.accept_states = set()

        self._minimize()

    def _minimize(self):
        """
        Minimize the given DFA using Hopcroft's algorithm.
        """
        # Step 1: Partition states into accepting and non-accepting sets
        partitions = [self.dfa.accept_states, set(self.dfa.transitions.keys()) - self.dfa.accept_states]

        # Step 2: Refine partitions
        while True:
            new_partitions = []
            for group in partitions:
                # Split group based on transitions
                split_groups = self._split_group(group, partitions)
                new_partitions.extend(split_groups)

            if new_partitions == partitions:
                break
            partitions = new_partitions

        # Step 3: Build the minimized DFA
        state_mapping = {state: f"S{index}" for index, group in enumerate(partitions, start=1) for state in group}
        self.start_state = state_mapping[self.dfa.start_state]
        self.accept_states = {state_mapping[state] for state in self.dfa.accept_states}

        for group in partitions:
            representative = next(iter(group))  # Pick any state as representative
            new_state = state_mapping[representative]
            self.minimized_transitions[new_state] = {}

            for symbol, target in self.dfa.transitions[representative].items():
                self.minimized_transitions[new_state][symbol] = state_mapping[target]

    def _split_group(self, group, partitions):
        """
        Split a group of states into smaller groups based on their transitions.
        """
        split_map = {}
        for state in group:
            # Create a signature for the state based on its transitions
            signature = tuple(
                next((i for i, part in enumerate(partitions) if target in part), -1)
                for symbol, target in self.dfa.transitions[state].items()
            )
            if signature not in split_map:
                split_map[signature] = set()
            split_map[signature].add(state)

        return list(split_map.values())

    def to_dict(self):
        """
        Convert the minimized DFA to a dictionary representation.
        """
        return {
            "start_state": self.start_state,
            "accept_states": list(self.accept_states),
            "transitions": self.minimized_transitions,
        }
    

def plot_minimized_dfa(minimized_dfa, output_folder):
    """
    Visualize the minimized DFA as a graph and save it as an image.
    """
    plot_fsm(
        transitions=minimized_dfa.minimized_transitions,
        start_state=minimized_dfa.start_state,
        accept_states=minimized_dfa.accept_states,
        file_name="minimized_dfa.png",
        output_folder=output_folder
    )

def save_minimized_dfa_to_json(minimized_dfa, file_name, output_folder):
    """
    Save the minimized DFA transitions and states to a JSON file with "isTerminatingState" for each state.
    """
    # Initialize the result dictionary
    dfa_dict = {"startingState": minimized_dfa.start_state}

    # Add states and transitions
    for state, transitions in minimized_dfa.minimized_transitions.items():
        state_entry = {"isTerminatingState": state in minimized_dfa.accept_states}
        for symbol, next_state in transitions.items():
            state_entry[symbol] = next_state
        dfa_dict[state] = state_entry

    # Save the JSON to a file
    json_path = os.path.join(output_folder, file_name)
    os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(dfa_dict, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":

    # Generate folder names by replacing *, |, and ? with _
    folder_names = [regex.replace("*", "_").replace("|", "_").replace("?", "_") for regex in regex_list]

    for regex, folder_name in zip(regex_list, folder_names):
        # Create output folder for each regex
        output_folder = os.path.join(os.getcwd(), "output", folder_name)
        os.makedirs(output_folder, exist_ok=True)

        # Build NFA and convert to DFA
        nfa = NFA().build_nfa_from_postfix(regex)
        dfa = DFA(nfa)
        minimized_dfa = MinimizedDFA(dfa)

        # Save nfa graph and JSON
        plot_nfa(nfa, "nfa.png", output_folder)
        save_nfa_to_json(nfa, "nfa.json", output_folder)

        # Save DFA graph and JSON
        plot_dfa(dfa, "dfa.png", output_folder)
        save_dfa_to_json(dfa, "dfa.json", output_folder)

        # Save minimized DFA graph and JSON
        plot_minimized_dfa(minimized_dfa,  output_folder)
        save_minimized_dfa_to_json(minimized_dfa, "minimized_dfa.json", output_folder)

