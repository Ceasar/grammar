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
