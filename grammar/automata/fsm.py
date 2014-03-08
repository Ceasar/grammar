

class FiniteStateAutomaton(object):
    def __init__(self, alphabet, states, start_state, transitions,
                 accepting_states):
        self.alphabet = alphabet
        self.states = states
        self.start_state = start_state
        self.transitions = transitions
        self.accepting_states = accepting_states

    def _recognizes(self, symbols):
        """Check if a machine recognizes a string."""
        current_states = {self.start_state}
        for symbol in symbols:
            new_states = current_states
            while new_states:
                new_states = {self.transitions[s, None] for s in new_states
                              if (s, None) in self.transitions}
                current_states |= new_states
            current_states = {self.transitions[s, symbol]
                              for s in current_states}
        return bool(current_states & self.accepting_states)

    def normalize(self, k=0):
        """
        Normalize a set by mapping all of its states to unique integers.
        """
        m = {state: i + k for i, state in enumerate(self.states)}
        return FiniteStateAutomaton(
            alphabet=self.alphabet,
            states=set(m.values()),
            start_state=k,
            transitions={(m[s], c): m[self.transitions[s, c]]
                         for c in self.alphabet for s in self.states},
            accepting_states={m[state] for state in self.accepting_states},
        )

    def union(self, other):
        """
        Combine two machines to recognize the union of their languages.

        :param other: A FSM.
        """
        a, b = self.normalize(), other.normalize(len(self.states))
        a.states |= b.states
        a.transitions.update(b.transitions)
        a.transitions[a.start_state, None] = b.start_state
        a.accepting_states |= b.accepting_states
        return a

    def concatenate(self, other):
        a, b = self.normalize(), other.normalize(len(self.states))
        a.states |= b.states
        a.transitions.update(b.transitions)
        for state in a.accepting_states:
            a.transitions[state, None] = b.start_state
        a.accepting_states = b.accepting_states
        return a

    def star(self):
        """
        Combine two machines to recognize the union of their languages.

        :param other: A FSM.
        """
        a = self.normalize()
        for state in a.accepting_states:
            a.transitions[state, None] = a.start_state
        a.accepting_states.add(a.start_state)
        return a

    def __contains__(self, s):
        return self._recognizes(s)

    def __add__(self, other):
        return self.concatenate(other)

    def __or__(self, other):
        return self.union(other)

    def __pos__(self):
        return self.star()

    def __repr__(self):
        return "FSM(%s, %s, %s, %s)" % (
            self.states,
            self.start_state,
            self.transitions,
            self.accepting_states,
        )
