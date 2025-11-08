class DFA:
    def __init__(self, nfa):
        self.states = set()
        self.transitions = dict()
        self.start_state = None
        self.accept_states = set()
        self.inputs = set()
        self._build_from_nfa(nfa)

    def print_definition(self):
        print(f"DFA Start State: {self.start_state}")
        print(f"DFA Accept States: {list(self.accept_states)}")
        print("DFA Transition Table:")
        print(f"{'State':<6} | {'Input':<6} | {'Next State':<10}")
        print("-"*40)
        for state in self.states:
            trans = self.transitions.get(state, {})
            for symbol, dst in trans.items():
                print(f"{state:<6} | {symbol:<6} | {dst:<10}")

    def _build_from_nfa(self, nfa):
        # Subset construction from NFA dict
        nfa_states = nfa["states"]
        nfa_start = nfa["start_state"]
        nfa_accepts = set(nfa["accept_states"])
        nfa_trans = nfa["transitions"]

        # Collect all input symbols except epsilon
        inputs = set()
        for trans in nfa_trans.values():
            inputs.update([k for k in trans.keys() if k != 'ε'])
        self.inputs = inputs

        # Helper: epsilon closure
        def epsilon_closure(states):
            stack = list(states)
            closure = set(states)
            while stack:
                state = stack.pop()
                for s in nfa_trans.get(state, {}).get('ε', []):
                    if s not in closure:
                        closure.add(s)
                        stack.append(s)
            return closure

        # Helper: move
        def move(states, symbol):
            result = set()
            for state in states:
                for t in nfa_trans.get(state, {}).get(symbol, []):
                    result.add(t)
            return result

        # Subset construction
        start = frozenset(epsilon_closure([nfa_start]))
        dfa_states = {start: "D1"}
        dfa_trans = {}
        unmarked = [start]
        state_id = 2
        accept_states = set()


        while unmarked:
            curr = unmarked.pop()
            curr_name = dfa_states[curr]
            dfa_trans[curr_name] = {}
            for symbol in inputs:
                next_states = frozenset(epsilon_closure(move(curr, symbol)))
                if not next_states:
                    # Transition to trap state for missing transitions
                    dfa_trans[curr_name][symbol] = "TRAP"
                    continue
                if next_states not in dfa_states:
                    dfa_states[next_states] = f"D{state_id}"
                    state_id += 1
                    unmarked.append(next_states)
                dfa_trans[curr_name][symbol] = dfa_states[next_states]

        # Add trap state if needed
        trap_needed = any(
            symbol not in dfa_trans[state]
            for state in dfa_trans
            for symbol in inputs
        ) or any("TRAP" in trans.values() for trans in dfa_trans.values())

        if trap_needed:
            trap_state = "TRAP"
            dfa_trans[trap_state] = {symbol: trap_state for symbol in inputs}

        for sset, name in dfa_states.items():
            if any(s in nfa_accepts for s in sset):
                accept_states.add(name)

        self.states = set(dfa_states.values())
        if trap_needed:
            self.states.add("TRAP")
        self.transitions = dfa_trans
        self.start_state = dfa_states[start]
        self.accept_states = accept_states

    def to_dict(self):
        return {
            "states": list(self.states),
            "start_state": self.start_state,
            "accept_states": list(self.accept_states),
            "inputs": list(self.inputs),
            "transitions": self.transitions
        }
