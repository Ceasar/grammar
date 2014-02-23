from automata.fsm import Transition, FiniteStateAutomaton as FSM

def _shunt(outputs, ps, symbols):
    if not symbols:
        return outputs[::-1] + ps
    elif not ps:
        if symbols[0] in {'(', '|', '&'}:
            return _shunt(outputs, ps + symbols[0], symbols[1:])
        else:
            return _shunt(symbols[0] + outputs, ps, symbols[1:])
    else:
        symbol, symbols = symbols[0], symbols[1:]
        if symbol == "(":
            return _shunt(outputs, '(' + ps, symbols)
        elif symbol == ")":
            ls, rs = "", ""
            for p in ps:
                if p == "(":
                    rs += p
                else:
                    ls += p
            return _shunt(ls + outputs, rs[1:], symbols)
        elif symbol == "|":
            if ps[0] == "(":
                return _shunt(outputs, '|' + ps, symbols)
            else:
                return _shunt(ps[0] + outputs, '|' + ps[1:], symbols)
        elif symbol == "&":
            return _shunt(outputs, '&' + ps, symbols)
        else:
            return _shunt(symbol+ outputs, ps, symbols)

def infix_to_postfix(infix):
    return _shunt("", "", infix)

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
