import itertools

import pytest

from fsm import FiniteStateAutomaton

# TODO: Add test for epsilons


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
        alphabet={'a', 'b'},
        states={0, 1, 2},
        start_state=0,
        transitions={
            (0, 'a'): 1,
            (0, 'b'): 2,
            (1, 'a'): 2,
            (1, 'b'): 2,
            (2, 'a'): 2,
            (2, 'b'): 2,
        },
        accepting_states={1},
    )
    return m 

@pytest.fixture
def n(m):
    """Recognizes 'b'."""
    m.transitions[0, 'a'] = 2
    m.transitions[0, 'b'] = 1
    return m 

@pytest.fixture(params=list(gen_words('ab')))
def s(request):
    return request.param


def test_accept(m, s):
    assert (s in m) == (s == 'a')


def test_union(m, n, s):
    assert (s in (m | n)) == (s in m or s in n)


def test_concatenation(m, n, s):
    assert (s in (m + n)) == any(
        s[:i] in m and s[i:] in m
        for i, _ in enumerate(s)
    )


def test_star(m, s):
    assert (s in (+m)) == (s.count('a') == len(s))
