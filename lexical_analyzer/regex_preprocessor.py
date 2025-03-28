""" 

- operator precedence:
    1. paranthesis: ()
    2. counters:    * + ?
    3. concetation: ab
    4. disjuntion:  a | b
    5. range        [] 
    
- use _ as concate operator as '.' mean anything
"""


def __tokenize_regex(regex:str) -> list[tuple[str, str]]:
    tokens = []
    i = 0
    while i < len(regex):
        if regex[i] == "-":                         #"a-z"
            tokens[-1] = (regex[i-1:i+2], "var")    # remove a & add a-z
            i += 2                                  # skip z                    
        elif regex[i] in "()[]*+?_|":
            tokens.append((regex[i], "op"))
            i += 1
        else:
            tokens.append((regex[i], "var"))
            i += 1
    return tokens

def __replace_range(tokens)  -> list[tuple[str, str]]:
    new_tokens = []
    inside_range = False
    var_before_me = False
    
    for val, type in tokens:
        if val == "[": inside_range = True
        elif val == "]": inside_range = False
        elif inside_range and var_before_me: new_tokens.append(("|", "op"))
    
        new_tokens.append((val, type))
        var_before_me = type == "var"
    return new_tokens

def __insert_concate(tokens: list[tuple[str, str]]) -> list[tuple[str, str]]:
    new_tokens = []
    for i in range(len(tokens)-1):
        new_tokens.append(tokens[i])
        curr_token, curr_type = tokens[i]
        nxt_token, nxt_type = tokens[i+1]

        if ((curr_type == "var" or curr_token in ")]*+?") 
            and (nxt_type == "var" or nxt_token in "([")) :
            new_tokens.append(("_", "op"))
    
    new_tokens.append(tokens[-1])
    return new_tokens



def infix_to_postfix(regex: str) -> str:
    operators = {"*": -1, "+": -2, "?": -3, "_": -4, "|": -5, "(": -100, "[": -100}
    
    tokens = __replace_range(__tokenize_regex(regex))
    tokens = __insert_concate(tokens)
    
    postfix_expr = []
    op_stack = []
    
    def pop_op_stack():
        postfix_expr.append(op_stack[-1])
        op_stack.pop()
        
    for (token, type) in tokens:
        if token in '([':
            op_stack.append(token)
            
        elif token in ')]':
            while op_stack[-1] not in '([': pop_op_stack()
            op_stack.pop()
            
        elif type == "op":
            while len(op_stack) != 0 and operators[token] <= operators[op_stack[-1]]:  pop_op_stack()
            op_stack.append(token)
            
        else:
            postfix_expr.append(token)
            
    while len(op_stack) != 0: pop_op_stack()
        
    return postfix_expr


if __name__ == "__main__":
    test_cases = [
        ("ab", ["a", "b", "_"]),
        ("a|b", ["a", "b", "|"]),
        ("(a|b)*", ["a", "b", "|", "*"]),
        ("a.b", ["a", ".", "_", "b", "_"]), 
        ("[a-z]?e", ["a-z", "?", "e", "_"]),
        ("a(b|c)*", ["a", "b", "c", "|", "*", "_"]),
    ]
    
    for infix, expected in test_cases:
        result = infix_to_postfix(infix)
        print(f"Input: {infix:<10} Output: {result}")
        assert result == expected, f"Failed for {infix}. Expected {expected}, got {result}"
    print("All tests passed!")