from collections import namedtuple

Transition = namedtuple("Transition", ["start", "end", "symbol"])


class FiniteStateAutomaton(object):
    def __init__(self, states, start_state, transitions, accepting_states):
        self.states = states
        self.start_state = start_state
        self.transitions = transitions
        self.accepting_states = accepting_states

    def closure(self, states):
        """
        Get the states reachable from epsilon transitions.
        """
        last_states = None
        while not states == last_states:
            last_states = states
            states |= {
                transition.end
                for transition in self.transitions
                for state in states
                if transition.start == state and transition.symbol is None
            }
        return states

    def run(self, symbols):
        """Get the set of final states."""
        states = self.closure({self.start_state})
        for symbol in symbols:
            states = self.closure({
                transition.end
                for transition in self.transitions
                for state in states
                if transition.start == state and transition.symbol == symbol
            })
        return states

    def accepts(self, string):
        """Check if a machine recognizes a string."""
        return bool(self.run(string) & self.accepting_states)

    def normalize(self, k=0):
        """
        Normalize a set by mapping all of its states to integers, starting with
        ``k``.
        """
        m = {state: i + k for i, state in enumerate(self.states)}
        return FiniteStateAutomaton(
            states=set(m.values()),
            start_state=k,
            transitions={Transition(m[start], m[end], symbol)
                        for start, end, symbol in self.transitions},
            accepting_states={m[state] for state in self.accepting_states},
        )

    def union(self, other):
        """
        Combine two machines to recognize the union of their languages.

        :param other: A FSM.
        """
        i, j = 0, len(self.states)
        a, b = self.normalize(i), other.normalize(j)
        return FiniteStateAutomaton(
            states=(a.states | b.states),
            start_state=i,
            transitions=(
                a.transitions |
                b.transitions |
                {Transition(i, j, None)}
            ),
            accepting_states=(a.accepting_states | b.accepting_states),
        )

    def __repr__(self):
        return "FSM(%s, %s, %s, %s)" % (
            self.states,
            self.start_state,
            self.transitions,
            self.accepting_states,
        )
