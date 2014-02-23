from grammar.regular import *



def test_infix_to_postfix_and():
    assert infix_to_postfix("x&y") == "xy&"

def test_infix_to_postfix_or():
    assert infix_to_postfix("x|y") == "xy|"

def test_infix_to_postfix_star():
    assert infix_to_postfix("x*") == "x*"

def test_infix_to_postfix_parens():
    assert infix_to_postfix("(x|y)") == "xy|"

def test_matches():
    assert matches("(x|y)", "x")
