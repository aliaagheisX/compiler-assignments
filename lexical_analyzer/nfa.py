from __future__ import annotations
from typing import Dict, Optional
from collections import deque, defaultdict
import json

import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import to_agraph

from regex_preprocessor import infix_to_postfix
from PIL import Image

class State:
    def __init__(self, state_num: int):
        self.transitions : Dict[str, list[State]] = defaultdict(list)
        self.state_name = f"S{state_num}"
    
    def add_transition(self, next_state: State, edge: str = "ε") -> None:
        self.transitions[edge].append(next_state)


class NFA:
    def __init__(self, start_counting_from = 0, initial_state = None, terminating_state = None):
        self.state_counter = start_counting_from
        self.initial_state: Optional[State] = initial_state
        self.terminating_state: Optional[State] = terminating_state
    
    def build_nfa_from_postfix(self, regex: list[str]):
        subsets = []
        op_compilers = {
            "*": self.compile_zero_or_more,
            "+": self.compile_one_or_more,
            "?": self.compile_zero_or_one,
            "_": self.compile_concat,
            "|": self.compile_or,
        }
    
        postfix = infix_to_postfix(regex)
        for token in postfix:
            if token in "|_": 
                subset = op_compilers[token](subsets[-2], subsets[-1])
                subsets.pop()
                subsets.pop()
                subsets.append(subset)
            elif token in "*+?": 
                subset = op_compilers[token](subsets[-1])
                subsets.pop()
                subsets.append(subset)
            else:
                subsets.append(self.compile_variable(token))
                
        return subsets[0]
        
    def create_state(self) -> State:
        """create a new state with auto-incremented counter"""
        state = State(self.state_counter)
        self.state_counter += 1
        return state
    
    def compile_variable(self, variable: str) -> NFA:
        """  S0 -- variable/character --> Se  """
        initial_state = self.create_state()
        terminating_state = self.create_state()
        
        initial_state.add_transition(terminating_state, variable)
        
        return NFA(
            initial_state=initial_state,
            terminating_state=terminating_state
        )
        
    def compile_zero_or_more(self, state: NFA) -> NFA:
        """  
            S0 -- state --> Se
             ^-------   
             -------------- ^  
        """
        initial_state = self.create_state()
        terminating_state = self.create_state()
        
        initial_state.add_transition(state.initial_state)
        initial_state.add_transition(terminating_state)
        
        state.terminating_state.add_transition(initial_state)
        state.terminating_state.add_transition(terminating_state)
        
        return NFA(
            initial_state=initial_state,
            terminating_state=terminating_state
        )
        
    def compile_one_or_more(self, state: NFA):
        """  
            S0 -- state --> Se
             ^-------   
        """
        initial_state = self.create_state()
        terminating_state = self.create_state()
        
        initial_state.add_transition(state.initial_state)
        
        state.terminating_state.add_transition(initial_state)
        state.terminating_state.add_transition(terminating_state)
        
        return NFA(
            initial_state=initial_state,
            terminating_state=terminating_state
        )
    
    def compile_zero_or_one(self, state: NFA):
        """  
            S0 -- state --> Se
            -------------- ^ 
        """
        initial_state = self.create_state()
        terminating_state = self.create_state()

        
        initial_state.add_transition(state.initial_state)
        initial_state.add_transition(terminating_state)
        state.terminating_state.add_transition(terminating_state)
        
        return NFA(
            initial_state=initial_state,
            terminating_state=terminating_state
        )
        
        
    def compile_concat(self, state1: NFA, state2: NFA) -> NFA:
        """  
            s1 ---> s2
        """
        output = state1
        
        output.terminating_state.add_transition(state2.initial_state)
        
        output.terminating_state = state2.terminating_state
        
        return output
    
    def compile_or(self, state1: NFA, state2: NFA):
        """  
                  state1
            S0 --/     \-->se
                 \     /
                  state2
        """
        initial_state = self.create_state()
        terminating_state = self.create_state()
        
        initial_state.add_transition(state1.initial_state)
        initial_state.add_transition(state2.initial_state)
        
        state1.terminating_state.add_transition(terminating_state)
        state2.terminating_state.add_transition(terminating_state)
        
        return NFA(
            initial_state=initial_state,
            terminating_state=terminating_state
        )
    
    def to_dict(self) -> dict:
        """Convert the NFA to a dictionary in the specified JSON format"""
        result = {  "startingState": self.initial_state.state_name }
        
        # BFS to collect all states
        visited, queue = set(), deque([self.initial_state])
        
        while queue:
            current_state = queue.popleft()
            
            if current_state.state_name in visited:  continue
            visited.add(current_state.state_name)
            
            state_entry = {"isTerminatingState": current_state == self.terminating_state}
            for edge, next_states in current_state.transitions.items():
                state_entry[edge] = [next_state.state_name for next_state in next_states]
                for next_state in next_states:
                    if next_state.state_name not in visited:
                        queue.append(next_state)
            
            result[current_state.state_name] = state_entry
        
        return result
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

def plot_nfa(nfa: NFA):
    data = nfa.to_dict()
    G = nx.DiGraph()

    # Add states (nodes)
    for state, transitions in data.items():
        if state == "startingState": continue
        G.add_node(state, shape="doublecircle" if transitions["isTerminatingState"] else "circle")
        
        for symbol, next_states in transitions.items():
            if symbol == "isTerminatingState": continue
            for next_state in next_states: 
                G.add_edge(state, next_state, label=symbol)
    A = to_agraph(G)
    # A.node_attr.update(style='filled', fillcolor='thistle', fontname='Helvetica', fontsize=14)
    # A.edge_attr.update(fontname='Helvetica', fontsize=12)
    
    # Set the initial state
    A.add_node("st", shape="none", label="")
    A.add_edge("st", data["startingState"])
    
    A.graph_attr.update(rankdir='LR')
    # Render and display
    A.layout(prog='dot')
    A.draw("nfa.png")
    
    return Image.open("nfa.png")

if __name__ == "__main__":
    regex = "(a|b)(c|d)?"

    result_nfa = NFA().build_nfa_from_postfix(regex)

    plot_nfa(result_nfa)