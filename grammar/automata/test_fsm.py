from finite_state_automaton import FiniteStateAutomaton, Transition


def test_accept():
    m = FiniteStateAutomaton(
        states={0, 1},
        start_state=0,
        transitions={Transition(0, 1, 'a')},
        accepting_states={1},
    )
    assert m.accepts("a")


def test_reject():
    m = FiniteStateAutomaton(
        states={0, 1},
        start_state=0,
        transitions={Transition(0, 1, 'a')},
        accepting_states={1},
    )
    assert not m.accepts("b")

def test_union():
    m = FiniteStateAutomaton(
        states={0, 1},
        start_state=0,
        transitions={Transition(0, 1, 'a')},
        accepting_states={1},
    )
    n = FiniteStateAutomaton(
        states={0, 1},
        start_state=0,
        transitions={Transition(0, 1, 'b')},
        accepting_states={1},
    )
    o = m.union(n)
    assert o.accepts("a")
    assert o.accepts("b")
    assert not o.accepts("ab")
