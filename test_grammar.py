import pytest

from grammar import Grammar, Production


@pytest.fixture
def grammar():
    S = 'S'
    NP = 'NP'
    VP = 'VP'
    T, N, V = 'T', 'N', 'V'
    productions = {
        Production(S, [NP, VP]),
        Production(NP, [T, N]),
        Production(VP, [V, NP]),
        Production(T, {'the'}),
        Production(N, {'man', 'ball'}),
        Production(V, {'hit', 'took'}),
    }
    grammar = Grammar(
        terminals={T, N, V},
        nonterminals={S, NP, VP},
        productions=productions,
        start=S,
    )
    return grammar


def test_tag(grammar):
    sentence = 'the man hit the man'
    got = list(grammar.tag(sentence.split()))
    expected = ['T', 'N', 'V', 'T', 'N']
    assert got == expected


def test_replace(grammar):
    nonterminal = 'NP'
    next_symbol = 'the'
    got = grammar.replace(nonterminal, next_symbol)
    expected = ['T', 'N']
    assert got == expected


def test_recognize(grammar):
    got = grammar.recognize('the man hit the ball')
    assert got == True
