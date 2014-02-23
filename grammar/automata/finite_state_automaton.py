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
        current_states = self.closure({self.start_state})
        for symbol in symbols:
            current_states = self.closure({
                transition.end
                for transition in self.transitions
                for state in current_states
                if transition.start == state and transition.symbol == symbol
            })
        return current_states

    def accepts(self, string):
        """Check if a machine recognizes a string."""
        return bool(self.run(string) & self.accepting_states)

    def normalize(self):
        """
        Normalize a set by mapping all of its states to unique integers.
        """
        m = {state: i + hash(self) for i, state in enumerate(self.states)}
        return FiniteStateAutomaton(
            states=set(m.values()),
            start_state=hash(self),
            transitions={Transition(m[start], m[end], symbol)
                        for start, end, symbol in self.transitions},
            accepting_states={m[state] for state in self.accepting_states},
        )

    def union(self, other):
        """
        Combine two machines to recognize the union of their languages.

        :param other: A FSM.
        """
        a, b = self.normalize(), other.normalize()
        return FiniteStateAutomaton(
            states=(a.states | b.states),
            start_state=a.start_state,
            transitions=(
                a.transitions |
                b.transitions |
                {Transition(a.start_state, b.start_state, None)}
            ),
            accepting_states=(a.accepting_states | b.accepting_states),
        )


    def star(self):
        """
        Combine two machines to recognize the union of their languages.

        :param other: A FSM.
        """
        a = self.normalize()
        start_state = min(a.states) - 1
        return FiniteStateAutomaton(
            states=a.states,
            start_state=start_state,
            transitions=(
                a.transitions |
                {Transition(start_state, a.start_state, None)} |
                {Transition(state, a.start_state, None)
                 for state in a.accepting_states}
            ),
            accepting_states=({start_state} | a.accepting_states),
        )

    def __add__(self, other):
        a, b = self.normalize(), other.normalize()
        return FiniteStateAutomaton(
            states=(a.states | b.states),
            start_state=a.start_state,
            transitions=(
                a.transitions |
                b.transitions |
                {Transition(state, b.start_state, None)
                 for state in a.accepting_states}
            ),
            accepting_states=b.accepting_states,
        )

    def __or__(self, other):
        return self.union(other)

    def __repr__(self):
        return "FSM(%s, %s, %s, %s)" % (
            self.states,
            self.start_state,
            self.transitions,
            self.accepting_states,
        )
