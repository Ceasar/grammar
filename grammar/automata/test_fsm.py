from finite_state_automaton import FiniteStateAutomaton, Transition


def test_accept():
    m = FiniteStateAutomaton({0, 1}, {Transition(0, 1, 'a')}, 0, {1})
    assert m.accepts("a")


def test_reject():
    m = FiniteStateAutomaton({0, 1}, {Transition(0, 1, 'a')}, 0, {1})
    assert not m.accepts("b")
