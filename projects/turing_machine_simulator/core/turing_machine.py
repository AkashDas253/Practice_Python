"""
A simple Turing Machine implementation in Python.
This example demonstrates a Turing machine that increments a binary number on the tape.
"""

class TuringMachine:
    def __init__(self, tm_def):
        self.tape = list(tm_def['tape'])
        self.head = 0
        self.state = tm_def['initial_state']
        self.transitions = tm_def['transitions']
        self.blank_symbol = tm_def['blank_symbol']
        self.final_states = set(tm_def['final_states'])

    def step(self):
        symbol = self.tape[self.head] if self.head < len(self.tape) else self.blank_symbol
        key = (self.state, symbol)
        if key in self.transitions:
            new_state, new_symbol, direction = self.transitions[key]
            if self.head < len(self.tape):
                self.tape[self.head] = new_symbol
            else:
                self.tape.append(new_symbol)
            self.state = new_state
            if direction == 'R':
                self.head += 1
            elif direction == 'L':
                self.head = max(0, self.head - 1)
        else:
            self.state = None  # Halt if no transition

    def run(self, max_steps=1000, verbose=False):
        steps = 0
        while self.state not in self.final_states and self.state is not None and steps < max_steps:
            if verbose:
                self.print_status()
            self.step()
            steps += 1
        if verbose:
            self.print_status()
        return ''.join(self.tape)

    def print_status(self):
        tape_str = ''.join(self.tape)
        head_str = ' ' * self.head + '^'
        print(f"Tape: {tape_str}\nHead: {head_str}\nState: {self.state}\n")

