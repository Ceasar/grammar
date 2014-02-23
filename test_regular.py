import pytest

from grammar.regular import *



def test_infix_to_postfix_and():
    assert infix_to_postfix("x&y") == "xy&"

def test_infix_to_postfix_or():
    assert infix_to_postfix("x|y") == "xy|"

def test_infix_to_postfix_star():
    assert infix_to_postfix("x*") == "x*"

def test_infix_to_postfix_parens1():
    assert infix_to_postfix("(x|y)") == "xy|"

def test_infix_to_postfix_parens2():
    assert infix_to_postfix("((x&y)|z)") == "xy&z|"

def test_infix_to_postfix_parens3():
    assert infix_to_postfix("(x&(y|z))") == "xyz|&"

def test_infix_to_postfix_parens4():
    assert infix_to_postfix("a&(b|(c&d))") == "abcd&|&"

def test_infix_to_postfix_mismatched_parens():
    with pytest.raises(SyntaxError):
        infix_to_postfix("a)")

def test_infix_to_postfix_not_enough_parens():
    with pytest.raises(SyntaxError):
        infix_to_postfix("(a")

def test_infix_to_postfix_case1():
    assert infix_to_postfix("((x))") == "x"

def test_infix_to_postfix_case2():
    assert infix_to_postfix("(x&y)") == "xy&"

def test_infix_to_postfix_case3():
    assert infix_to_postfix("x&y&z") == "xyz&&"

def test_infix_to_postfix_case4():
    assert infix_to_postfix("x|y|z") == "xyz||"

def test_matches_trivial():
    assert matches("x", "x")
    assert not matches("x", "")
    assert not matches("x", "y")

def test_matches_star():
    assert matches("x*", "")
    assert matches("x*", "x")
    assert matches("x*", "xx")
    assert not matches("x*", "y")

def test_matches_union1():
    assert matches("x|y|z", "x")

def test_matches_union2():
    assert matches("x|y|z", "y")

def test_matches_union3():
    assert matches("x|y|z", "z")

def test_matches_union4():
    assert not matches("x|y|z", "d")

def test_matches_concatenation():
    assert matches("x&y&z", "xyz")
    assert not matches("x&y&z", "")
    assert not matches("x&y&z", "x")
    assert not matches("x&y&z", "xy")
    assert not matches("x&y&z", "d")
