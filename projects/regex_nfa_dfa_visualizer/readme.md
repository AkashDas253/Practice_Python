# Regex → NFA → DFA Converter + Visualizer

A Python tool to convert regular expressions into finite automata and visualize their transitions. Useful for learning, teaching, and experimenting with automata theory.

## Features
- **Regex to NFA:** Build an NFA from a regular expression using Thompson’s construction.
- **NFA to DFA:** Convert the NFA to a DFA using subset construction (with trap state for completeness).
- **Visualization:** Print readable automata transitions; extendable to graphical visualization with `graphviz` or `networkx`.
- **Step-by-step Animation:** (Planned) Animate transitions for educational clarity.
- **Interactive Mode:** (Planned) Visual playground for automata.

## Getting Started

### Prerequisites
- Python 3.7+
- (Optional) `graphviz` or `networkx` for graphical visualization

### Installation
Clone the repository:
```sh
git clone https://github.com/AkashDas253/Practice_Python.git
```
Navigate to the project folder:
```sh
cd Practice_Python/projects/regex_nfa_dfa_visualizer
```
Install dependencies (if using visualization extras):
```sh
pip install graphviz networkx
```

### Usage
Run the main script:
```sh
python main.py
```
Follow the prompts to enter a regex and view the NFA/DFA transitions.

## Project Structure
```
core/
    nfa.py            # NFA construction and logic
    dfa.py            # DFA construction and logic
    regex_parser.py   # Regex parsing utilities
    visualizer.py     # Text-based automata visualization
main.py               # Entry point for CLI usage
```

## Code Overview

### RegexParser (`core/regex_parser.py`)
- Converts infix regex to postfix (Shunting Yard algorithm)
- Adds explicit concatenation operators

### NFA (`core/nfa.py`)
- Builds NFA from regex (Thompson’s construction)
- Handles states, transitions, and epsilon moves

### DFA (`core/dfa.py`)
- Converts NFA to DFA (subset construction)
- Ensures all transitions are present (trap state)

### AutomataVisualizer (`core/visualizer.py`)
- Prints automata states and transitions in readable format

## Contributing
Pull requests and suggestions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
MIT License
