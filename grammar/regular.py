from automata.fsm import Transition, FiniteStateAutomaton as FSM


def _shunt(symbols):
    outputs = ''
    ps = ''
    for symbol in symbols:
        if ps:
            if symbol == '(':
                ps = '(' + ps
            elif symbol == ')':
                rs = ''
                for p in ps:
                    if p == '(':
                        rs += p
                    else:
                        outputs += p
                ps = rs[1:]
            elif symbol == '|':
                if ps[0] == '(':
                    ps = '|' + ps
                else:
                    outputs += '('
                    ps = '|' + ps[1:]
            elif symbol == '&':
                ps = '&' + ps
            else:
                outputs += symbol
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
            ms.append(ms.pop() + ms.pop())
        elif symbol == '*':
            ms.append(+ms.pop())
        elif symbol == '@':
            pass
        else:
            ms.append(FSM(
                states={0, 1},
                start_state=0,
                transitions={Transition(0, 1, symbol)},
                accepting_states={1},
            ))
    return ms.pop()

def matches(infix, string):
    fsm = postfix_to_fsm(infix_to_postfix(infix))
    return fsm.recognizes(string)
