from fsm import FiniteStateAutomaton, Transition


def test_accept():
    m = FiniteStateAutomaton(
        states={0, 1},
        start_state=0,
        transitions={Transition(0, 1, 'a')},
        accepting_states={1},
    )
    assert m.recognizes("a")


def test_reject():
    m = FiniteStateAutomaton(
        states={0, 1},
        start_state=0,
        transitions={Transition(0, 1, 'a')},
        accepting_states={1},
    )
    assert not m.recognizes("b")


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
    o = m | n
    assert o.recognizes("a")
    assert o.recognizes("b")
    assert not o.recognizes("c")


def test_concatenation():
    m = FiniteStateAutomaton(
        states={0, 1},
        start_state=0,
        transitions={Transition(0, 1, 'a'),},
        accepting_states={1},
    )
    n = FiniteStateAutomaton(
        states={0, 1},
        start_state=0,
        transitions={Transition(0, 1, 'b'),},
        accepting_states={1},
    )
    o = m + n
    assert not o.recognizes("a")
    assert not o.recognizes("b")
    assert o.recognizes("ab")
    assert not o.recognizes("ba")


def test_star():
    m = FiniteStateAutomaton(
        states={0, 1},
        start_state=0,
        transitions={
            Transition(0, 1, 'a'),
        },
        accepting_states={1},
    )
    n = +m
    assert n.recognizes("")
    assert n.recognizes("a")
    assert n.recognizes("aa")
    assert not n.recognizes("b")
