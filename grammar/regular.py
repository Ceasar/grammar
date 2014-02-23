from automata.fsm import Transition, FiniteStateAutomaton as FSM


def infix_to_postfix(symbols):
    outputs = ''
    stack = []
    for symbol in symbols:
        if symbol == ')':
            new_stack = []
            for p in reversed(stack):
                if p == '(':
                    new_stack.append(p)
                else:
                    outputs += p
            stack = new_stack
            try:
                stack.pop()
            except IndexError:
                raise SyntaxError("mismatched parenthesis")
        elif symbol in {'(', '|', '&'}:
            stack.append(symbol)
        else:
            outputs += symbol
    if "(" in stack:
        raise SyntaxError("unmatched parenthesis")
    return outputs + ''.join(stack)


def postfix_to_fsm(symbols):
    ms = []
    for symbol in symbols:
        if symbol == '|':
            ms.append(ms.pop() | ms.pop())
        elif symbol == '&':
            m1 = ms.pop()
            m2 = ms.pop()
            ms.append(m2 + m1)
        elif symbol == '*':
            ms.append(+ms.pop())
        else:
            ms.append(FSM(
                states={0, 1},
                start_state=0,
                transitions={Transition(0, 1, symbol)},
                accepting_states={1},
            ))
    return ms.pop()


def _make_fsm(infix):
    return postfix_to_fsm(infix_to_postfix(infix))


def matches(infix, string):
    fsm = _make_fsm(infix)
    return fsm.recognizes(string)
