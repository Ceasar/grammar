from automata.fsm import Transition, FiniteStateAutomaton as FSM

def _shunt(outputs, ps, symbols):
    if not symbols:
        outputs.reverse()
        return "".join(outputs + ps)
    elif not ps:
        symbol = symbols[0]
        if symbol in {'(', '|', '&'}:
            ps.append(symbol)
            return _shunt(outputs, ps, symbols[1:])
        else:
            return _shunt([symbol] + outputs, [], symbols[1:])
    else:
        symbol = symbols[0]
        p = ps[0]
        xs = symbols[1:]
        if symbol == "(":
            return _shunt(outputs, [symbol] + ps, xs)
        elif symbol == ")":
            ls, rs = [], []
            for x in ps:
                if x == "(":
                    rs.append(x)
                else:
                    ls.append(x)
                    return _shunt(ls + outputs, rs[1:], xs)
        elif symbol == "|":
            if p == "(":
                return _shunt(outputs, [symbol] + ps, xs)
            else:
                return _shunt([p] + outputs, [symbol] + ps[1:], xs)
        elif symbol == "&":
            return _shunt(outputs, [symbol] + ps, xs)
        else:
            return _shunt([symbol] + outputs, ps, xs)

def infix_to_postfix(infix):
    return _shunt([], [], infix)

def postfix_to_fsm(postfix):
    ms = []
    for char in postfix:
        if char == '|':
            m1 = ms.pop()
            m2 = ms.pop()
            ms.append(m1 | m2)
        elif char == '&':
            m1 = ms.pop()
            m2 = ms.pop()
            ms.append(m1 + m2)
        elif char == '*':
            m1 = ms.pop()
            ms.append(+m1)
        elif char == '@':
            pass
        else:
            fsm = FSM(
                states={0, 1},
                start_state=0,
                transitions={Transition(0, 1, char)},
                accepting_states={1},
            )
            ms.append(fsm)
    return ms[0]

def matches(infix, string):
    postfix = infix_to_postfix(infix)
    fsm = postfix_to_fsm(postfix)
    return fsm.recognizes(string)
