"""
Demonstration of LL parsing algorithm.

This doesn't construct an AST-- it just checks if a word is recognized.
"""


class Production(object):
    def __init__(self, head, body):
        self.head = head
        self.body = body

    def __repr__(self):
        return "%s -> %s" % (self.head, self.body)


class Grammar(object):
    def __init__(self, terminals, nonterminals, productions, start):
        self.terminals = terminals
        self.nonterminals = nonterminals
        self.productions = productions
        self.start = start

    def _matching_productions(self, symbol):
        return {production for production in self.productions
                if production.head == symbol}


    def _follow(self, symbol):
        productions = list(self._matching_productions(symbol))
        print "productions: ", productions
        production = productions[0]
        print "production: ", production
        token = production.body[0]
        return (symbol if symbol in self.productions else self._follow(token))

    @property
    def parse_table(self):
        parse_table = {}
     
        for production in self.productions:
            head, body = production.head, production.body
            # parse_table[head, self._follow(body[0])] = body
            parse_table[head, body[0]] = body
     
        return parse_table

    def recognize(self, string):
        return self.derive(self.tag(string.split()))

    def replace(self, nonterminal, next_symbol):
        productions = list(self._matching_productions(nonterminal))
        if len(productions) == 1:
            return productions[0].body
        else:
            raise SyntaxError()

    def tag(self, words):
        for word in words:
            for terminal in self.terminals:
                production = self._matching_productions(terminal).pop()
                if word in production.body:
                    yield terminal
                    continue

    def derive(self, symbols):
        stack = [self.start]
        next_symbol = next(symbols)
        while len(stack) > 0:
            top = stack.pop()
            if top in self.nonterminals:
                stack.extend(reversed(self.replace(top, next_symbol)))
            else:
                if next_symbol == top:
                    # discard both
                    try:
                        next_symbol = next(symbols)
                    except StopIteration:
                        return len(stack) == 0
                else:
                    raise SyntaxError("Ungrammatical sentence.")

    def __repr__(self):
        return "Grammar(%s, %s, %s, %s)" % (
            self.terminals,
            self.nonterminals,
            self.productions,
            self.start,
        )
