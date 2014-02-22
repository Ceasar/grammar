"""
Demonstration of LL parsing algorithm.

This doesn't construct an AST-- it just checks if a word is recognized.
"""


def build_parse_table(grammar):
    """
    >>> grammar = {
    ... 'S': ['F', '( S + F )'],
    ... 'F': ['a'],
    ... }
    >>> build_parse_table(grammar)
    {('S', 'a'): 'F', ('F', 'a'): 'a', ('S', '('): '( S + F )'}
    """
    parse_table = {}
 
    def _follow(symbol):
        return symbol if symbol in grammar else _follow(grammar[symbol][0][0])
 
    for lhs in grammar:
        for rhs in grammar[lhs]:
            parse_table[lhs, _follow(rhs[0])] = rhs
 
    return parse_table
 
 
def ll_parse(parse_table):
    """
    >>> grammar = {
    ... 'S': ['F', '( S + F )'],
    ... 'F': ['a'],
    ... }
    >>> parse = ll_parse(build_parse_table(grammar))
    >>> parse('( a + a )'.split())
    True
    """
    def parser(input_buffer):
        stack = ['S']
        ins = iter(input_buffer)
        look_ahead = next(ins)
        while len(stack) > 0:
            top = stack.pop()
            if look_ahead == top:
                # discard both
                try:
                    look_ahead = next(ins)
                except StopIteration:
                    return len(stack) == 0
            else:
                try:
                    rhs = parse_table[top, look_ahead]
                except KeyError:
                    raise SyntaxError()
                else:
                    stack.extend(reversed(rhs.split()))
    return parser
