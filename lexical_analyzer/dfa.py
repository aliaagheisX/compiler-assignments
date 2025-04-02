import os
import json
from typing import Dict, Set, List
from collections import deque
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
from nfa import NFA
from utils import plot_fsm

class DFA:
    def __init__(self, nfa):
        """
        Initialize the DFA with an NFA as input.
        """
        self.nfa = nfa
        self.states: Dict[frozenset, str] = {}  # Maps sets of NFA states to DFA state names
        self.transitions: Dict[str, Dict[str, str]] = {}  # DFA transitions
        self.start_state: str = None
        self.accept_states: Set[str] = set()

        self._convert_nfa_to_dfa()
        self.rename_states()

    def _convert_nfa_to_dfa(self):
        """
        Convert the given NFA to a DFA using the subset construction algorithm.
        """
        # Step 1: Compute the epsilon-closure of the NFA's start state
        start_closure = self._epsilon_closure({self.nfa.initial_state})
        start_state_name = self._get_state_name(start_closure)
        self.start_state = start_state_name
        self.states[frozenset(start_closure)] = start_state_name
        self.transitions[start_state_name] = {}

        # Step 2: Perform BFS to explore all DFA states
        queue = deque([start_closure])
        while queue:
            current_closure = queue.popleft()
            current_state_name = self._get_state_name(current_closure)

            # Group transitions by symbol
            symbol_to_states = {}
            for state in current_closure:
                for symbol, next_states in state.transitions.items():
                    if symbol != "ε":  # Ignore epsilon transitions
                        if symbol not in symbol_to_states:
                            symbol_to_states[symbol] = set()
                        symbol_to_states[symbol].update(next_states)

            # Process transitions for each symbol
            for symbol, next_states in symbol_to_states.items():
                next_closure = self._epsilon_closure(next_states)
                next_state_name = self._get_state_name(next_closure)

                if frozenset(next_closure) not in self.states:
                    self.states[frozenset(next_closure)] = next_state_name
                    self.transitions[next_state_name] = {}
                    queue.append(next_closure)

                self.transitions[current_state_name][symbol] = next_state_name

            # Mark as accepting state if any NFA state in the closure is accepting
            if any(state == self.nfa.terminating_state for state in current_closure):
                self.accept_states.add(current_state_name)

    def _epsilon_closure(self, states: Set) -> Set:
        """
        Compute the epsilon-closure of a set of NFA states.
        """
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            for next_state in state.transitions.get("ε", []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

        return closure

    def _get_state_name(self, states: Set) -> str:
        """
        Generate a unique name for a set of NFA states.
        """
        return "_".join(sorted(state.state_name for state in states))
    
    def rename_states(self):
        """
        Rename DFA states to a more readable format (e.g., S1, S2, ...).
        Updates the DFA's transitions, start state, and accept states.
        """
        # Create a mapping from old state names to new state names
        state_mapping = {}
        for index, old_state in enumerate(self.transitions.keys(), start=1):
            state_mapping[old_state] = f"S{index}"

        # Update transitions with new state names
        new_transitions = {}
        for old_state, transitions in self.transitions.items():
            new_state = state_mapping[old_state]
            new_transitions[new_state] = {
                symbol: state_mapping[next_state] for symbol, next_state in transitions.items()
            }

        # Update start state and accept states
        self.start_state = state_mapping[self.start_state]
        self.accept_states = {state_mapping[old_state] for old_state in self.accept_states}
        self.transitions = new_transitions
    

def plot_dfa(dfa, file_name, output_folder):
    """
    Visualize the DFA as a graph and save it as an image using the common plot_fsm function.
    """
    plot_fsm(
        transitions=dfa.transitions,
        start_state=dfa.start_state,
        accept_states=dfa.accept_states,
        file_name=file_name,
        output_folder=output_folder
    )


def save_dfa_to_json(dfa, file_name, output_folder):
    """
    Save the DFA transitions and states to a JSON file in the specified format.
    """
    # Initialize the result dictionary
    dfa_dict = {"startingState": dfa.start_state}

    # Add states and transitions
    for state, transitions in dfa.transitions.items():
        state_entry = {"isTerminatingState": state in dfa.accept_states}
        for symbol, next_state in transitions.items():
            state_entry[symbol] = next_state
        dfa_dict[state] = state_entry

    # Save the JSON to a file
    json_path = os.path.join(output_folder, file_name)
    with open(json_path, "w") as json_file:
        json.dump(dfa_dict, json_file, indent=4)
