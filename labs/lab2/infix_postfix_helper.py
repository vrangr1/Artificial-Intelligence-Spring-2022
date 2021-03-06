import cnf_helper
import re
def add_required_spaces(bnf_string: str) -> str:
    """
        Add spaces around brackets and operators
    """
    for operator in cnf_helper.ALL_OPERATORS:
        if operator == cnf_helper.IMPLIES:
            continue
        bnf_string = bnf_string.replace(operator, " " + operator + " ")
    occurrences = [m.start() for m in re.finditer(cnf_helper.IMPLIES, bnf_string)]
    occurrences.sort()
    num = 0
    for index in occurrences:
        index += num
        if bnf_string[index - 1] == '<':
            continue
        bnf_string = bnf_string[:index] + " " + bnf_string[index:]
        num += 1
    bnf_string = bnf_string.replace(" " + cnf_helper.IMPLIES, " " + cnf_helper.IMPLIES + " ")
    bnf_string = bnf_string.replace("(", " ( " )
    bnf_string = bnf_string.replace(")", " ) ")
    return bnf_string


def infix_to_postfix(infix: str):
    # Add spaces around operators and brackets
    infix = add_required_spaces(infix)
    # Split the string into tokens
    infix = infix.strip().split()
    conversion_stack = list()
    postfix = list()
    for token in infix:
        if token == '(':
            conversion_stack.append(token)
        elif token == ')':
            while len(conversion_stack) > 0 and conversion_stack[-1] != '(':
                postfix.append(conversion_stack.pop())
            conversion_stack.pop()
        elif cnf_helper.is_atom(token):
            postfix.append(token)
            continue
        else:
            while len(conversion_stack) > 0 and conversion_stack[-1] != '(' and not cnf_helper.higher_precedence(token, conversion_stack[-1]):
                postfix.append(conversion_stack.pop())
            conversion_stack.append(token)
    while not len(conversion_stack) == 0:
        postfix.append(conversion_stack.pop())
    return postfix

def postfix_to_infix(postfix: list) -> str:
    conversion_stack = []
    for token in postfix:
        if cnf_helper.is_atom(token):
            conversion_stack.append(token)
            continue
        if token == cnf_helper.NEGATION:
            cur_val = cnf_helper.NEGATION + conversion_stack.pop() 
            conversion_stack.append(cur_val)
        else:
            second = conversion_stack.pop()
            first = conversion_stack.pop()
            conversion_stack.append("(" + first + " " + token + " " + second + ")")
    return conversion_stack.pop()