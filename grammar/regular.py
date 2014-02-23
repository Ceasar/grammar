from automata.fsm import Transition, FiniteStateAutomaton as FSM


def _shunt(symbols):
    outputs = ''
    ps = ''
    for symbol in symbols:
        if ps and symbol in ('(', ')'):
            if symbol == '(':
                ps += '('
            else:
                pass
                rs = ''
                for p in ps:
                    if p == '(':
                        rs += p
                    else:
                        outputs += p
                ps = rs[1:]
        elif symbol in {'(', '|', '&'}:
            ps += symbol
        else:
            outputs += symbol
    return outputs + ps


def infix_to_postfix(infix):
    return _shunt(infix)

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
