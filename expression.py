from nfa import *

def postfix_to_nfa(postfix):
    stack = []
    for char in postfix:
        if char in alphabet:

            s1 = State(get_next_state_tag(), isstart=True)
            s2 = State(get_next_state_tag(), isfinal=True)
            t1 = Transition(s2, char)
            s1.transitions.add(t1)
            _nfa = NFA([s1, s2])
            stack.append(_nfa)

        elif char == '.':
            x2 = stack.pop()
            x1 = stack.pop()
            stack.append(concat(x1,x2))

        elif char == '|':
            x2 = stack.pop()
            x1 = stack.pop()
            stack.append(slash(x1, x2))

        elif char == '*':
            x1 = stack.pop()
            stack.append(star(x1))

        print "_____________________________________"
        print stack[len(stack) - 1]

    if stack:
        nfa = stack.pop()
        return nfa


def re_to_postfix(infix):
    precedence = {'*': 3, '+': 3, '?': 3, '.': 2, '|': 1}
    operators = precedence.keys()
    binary_operators = ['|', '.']
    unary_operators = ['?', '*', '+']

    stack = []
    output = []

    i = 0
    while i < len(infix):
        e = infix[i]
        if e in alphabet:
            output.append(e)
        elif e in operators:
            o1 = e
            while stack and stack[-1] in operators:
                o2 = stack[-1]
                if o1 in binary_operators and precedence[o2] >= precedence[o1] or \
                                        o1 in unary_operators and precedence[o2] > precedence[o1]:
                    output.append(stack.pop())
                else:
                    break
            stack.append(e)
        elif e == '(':
            stack.append(e)
        elif e == ')':
            stack_element = stack.pop()
            while stack_element != '(':
                output.append(stack_element)
                stack_element = stack.pop()
        i += 1
    while stack:
        top = stack.pop()
        if top != '(':
            output.append(top)
    return output
