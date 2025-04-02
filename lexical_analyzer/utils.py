import json
from collections import deque

def load_json(file_path):
    """
    Load a JSON file from the given file path.
    :param file_path: Path to the JSON file.
    :return: Parsed JSON object.
    """
    with open(file_path, "r") as file:
        return json.load(file)

def load_json(file_path):
    """
    Load a JSON file from the given file path.
    :param file_path: Path to the JSON file.
    :return: Parsed JSON object.
    """
    with open(file_path, "r") as file:
        return json.load(file)

def compare_automata_json(json1: dict, json2: dict) -> bool:
    """
    Compare two automata JSONs to check if they are structurally identical
    by comparing the number of transitions at each level of traversal.
    """
    # Get starting states
    start1 = json1.get("startingState")
    start2 = json2.get("startingState")
    
    if not start1 or not start2:
        return False  # Invalid automata
    
    # Helper to get all transition symbols for a state (excluding special properties)
    def get_symbols(json_data, state):
        if state not in json_data:
            return set()
        return {k for k in json_data[state].keys() if k != "isTerminatingState"}
    
    # Helper to check if a state is accepting
    def is_accepting(json_data, state):
        if state not in json_data:
            return False
        return json_data[state].get("isTerminatingState", False)
    
    # BFS traversal to compare structure level by level
    queue1 = deque([start1])
    queue2 = deque([start2])
    visited1 = {start1}
    visited2 = {start2}
    
    # Starting states must have same termination status
    if is_accepting(json1, start1) != is_accepting(json2, start2):
        return False
    
    while queue1 and queue2:
        # Make sure both queues have the same size at each level
        if len(queue1) != len(queue2):
            return False
        
        level_size = len(queue1)
        
        # Process all states at current level
        for _ in range(level_size):
            current1 = queue1.popleft()
            current2 = queue2.popleft()
            
            # Both states must have same accepting status
            if is_accepting(json1, current1) != is_accepting(json2, current2):
                return False
            
            # Both states must have same outgoing symbols
            symbols1 = get_symbols(json1, current1)
            symbols2 = get_symbols(json2, current2)
            
            if symbols1 != symbols2:
                return False
            
            # For each symbol, count transitions and add new states to queue
            for symbol in symbols1:
                targets1 = json1[current1].get(symbol)
                targets2 = json2[current2].get(symbol)
                
                # Convert to lists for consistent handling
                if not isinstance(targets1, list):
                    targets1 = [targets1]
                if not isinstance(targets2, list):
                    targets2 = [targets2]
                
                # Must have same number of transitions for each symbol
                if len(targets1) != len(targets2):
                    return False
                
                # Add new states to visit
                for target1 in targets1:
                    if target1 not in visited1:
                        visited1.add(target1)
                        queue1.append(target1)
                
                for target2 in targets2:
                    if target2 not in visited2:
                        visited2.add(target2)
                        queue2.append(target2)
    
    # Both queues should be empty if graph structure is identical
    return len(queue1) == len(queue2) == 0