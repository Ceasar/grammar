import pytest

from grammar.regular import *


def test_matches_trivial1():
    re = "x"
    assert matches(re, "x")
    assert not matches(re, "")
    assert not matches(re, "y")

def test_matches_trivial2():
    re = "(x)"
    assert matches(re, "x")
    assert not matches(re, "")
    assert not matches(re, "y")

def test_matches_trivial3():
    re = "((x))"
    assert matches(re, "x")
    assert not matches(re, "")
    assert not matches(re, "y")

def test_matches_star():
    assert matches("a*", "")
    assert matches("a*", "a")
    assert matches("a*", "aa")
    assert not matches("a*", "b")

def test_matches_union0():
    assert matches("a|b", "a")
    assert matches("a|b", "b")

def test_matches_union1():
    assert matches("(a|b)", "a")
    assert matches("(a|b)", "b")

def test_matches_union2():
    re = "x|y|z"
    assert matches(re, "x")
    assert matches(re, "y")
    assert matches(re, "z")
    assert not matches(re, "d")
    assert not matches(re, "xy")

def test_matches_concatenation1():
    re = "a&b"
    assert matches(re, "ab")

def test_matches_concatenation2():
    re = "a&b&c"
    assert matches(re, "abc")
    assert not matches(re, "")
    assert not matches(re, "a")
    assert not matches(re, "ab")
    assert not matches(re, "d")

def test_complex1():
    re = "((x&y)|z)"
    assert matches(re, "xy")
    assert matches(re, "z")

def test_complex2():
    re = "(x&(y|z))"
    assert matches(re, "xy")
    assert matches(re, "xz")

def test_complex3():
    re = "a&(b|(c&d))"
    assert matches(re, "ab")
    assert matches(re, "acd")

def test_mismatched_parens():
    with pytest.raises(SyntaxError):
        matches("a)", "a")

def test_not_enough_parens():
    with pytest.raises(SyntaxError):
        matches("(a", "a")
