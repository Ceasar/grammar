from collections import namedtuple

Transition = namedtuple("Transition", ["start", "end", "symbol"])


class FiniteStateAutomaton(object):
    def __init__(self, states, transitions, start_state, accepting_states):
        self.states = states
        self.transitions = transitions
        self.start_state = start_state
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

    def union(self, other):
        states = set(range(len(self.states) + len(other.states) + 1))
        start_state = 0

        m1 = {}
        for i, state in enumerate(self.states):
            m1[state] = i + 1
        m2 = {}
        for i, state in enumerate(other.states):
            m2[state] = i + 1 + len(self.states)

        transitions = set()
        for transition in self.transitions:
            start, end, symbol = transition
            transitions.add(Transition(m1[start], m1[end], symbol))
        for transition in other.transitions:
            start, end, symbol = transition
            transitions.add(Transition(m2[start], m2[end], symbol))
        transitions.add(Transition(0, 1, None))
        transitions.add(Transition(0, 1 + len(self.states), None))

        accepting_states = set()
        for state in self.accepting_states:
            accepting_states.add(m1[state])
        for state in self.accepting_states:
            accepting_states.add(m2[state])

        return FiniteStateAutomaton(states, transitions, start_state,
                                    accepting_states)
