from finite_state_automaton import FiniteStateAutomaton, Transition


def test_accept():
    m = FiniteStateAutomaton({0, 1}, {Transition(0, 1, 'a')}, 0, {1})
    assert m.accepts("a")


def test_reject():
    m = FiniteStateAutomaton({0, 1}, {Transition(0, 1, 'a')}, 0, {1})
    assert not m.accepts("b")

def test_union():
    m = FiniteStateAutomaton({0, 1}, {Transition(0, 1, 'a')}, 0, {1})
    n = FiniteStateAutomaton({0, 1}, {Transition(0, 1, 'b')}, 0, {1})
    o = m.union(n)
    assert o.accepts("a")
    assert o.accepts("b")
    assert not o.accepts("ab")
