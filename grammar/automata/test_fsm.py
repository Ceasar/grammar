import itertools

import pytest

from fsm import FiniteStateAutomaton, Transition


def gen_words(alphabet, limit=4):
    n = 0
    while n < limit:
        for s in itertools.product(alphabet, repeat=n):
            yield ''.join(s)
        n += 1

@pytest.fixture
def m():
    """Recognizes 'a'."""
    m = FiniteStateAutomaton(
        states={0, 1, 2},
        start_state=0,
        transitions={
            Transition(0, 1, 'a'),
            Transition(0, 2, 'b'),
            Transition(1, 2, 'a'),
            Transition(1, 2, 'b'),
            Transition(2, 2, 'a'),
            Transition(2, 2, 'b'),
        },
        accepting_states={1},
    )
    return m 

@pytest.fixture
def n():
    """Recognizes 'b'."""
    m = FiniteStateAutomaton(
        states={0, 1, 2},
        start_state=0,
        transitions={
            Transition(0, 2, 'a'),
            Transition(0, 1, 'b'),
            Transition(1, 2, 'a'),
            Transition(1, 2, 'b'),
            Transition(2, 2, 'a'),
            Transition(2, 2, 'b'),
        },
        accepting_states={1},
    )
    return m 

@pytest.fixture(params=gen_words('ab'))
def s(request):
    return request.param


def test_accept(m, s):
    assert m.recognizes(s) == (s == 'a')


def test_union(m, n, s):
    assert (m | n).recognizes(s) == (m.recognizes(s) or n.recognizes(s))


def test_concatenation(m, n, s):
    assert (m + n).recognizes(s) == any(
        m.recognizes(s[:i]) and n.recognizes(s[i:])
        for i, _ in enumerate(s)
    )


def test_star(m, s):
    assert (+m).recognizes(s) == (s.count('a') == len(s))


def test_epsilon():
    m = FiniteStateAutomaton(
        states=set([0, 1, 2, 3, 4, 5]),
        start_state=0,
        transitions=set([
            Transition(start=0, end=1, symbol='c'),
            Transition(start=0, end=2, symbol=None),
            Transition(start=2, end=3, symbol='b'),
            Transition(start=2, end=4, symbol=None),
            Transition(start=4, end=5, symbol='a'),
        ]),
        accepting_states=set([1, 3, 5]),
    )
    assert m.recognizes("a")
    assert m.recognizes("b")
    assert m.recognizes("c")
    assert not m.recognizes("d")
