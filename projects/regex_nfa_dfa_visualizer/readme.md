# Regex → NFA → DFA Converter + Visualizer

A Python tool to convert regular expressions into finite automata and visualize their transitions. Useful for learning, teaching, and experimenting with automata theory.

## Features
- **Regex to NFA:** Build an NFA from a regular expression using Thompson’s construction.
- **NFA to DFA:** Convert the NFA to a DFA using subset construction (with trap state for completeness).
- **Visualization:** Print readable automata transitions; graphical visualization using `networkx` and `matplotlib` (no external binaries required).
- **Step-by-step Animation:** (Planned) Animate transitions for educational clarity.
- **Interactive Mode:** (Planned) Visual playground for automata.

## Getting Started

### Prerequisites
- Python 3.7+
- `networkx>=3.0`
- `matplotlib>=3.7`

### Installation
Clone the repository:
```sh
git clone https://github.com/AkashDas253/Practice_Python.git
```
Navigate to the project folder:
```sh
cd Practice_Python/projects/regex_nfa_dfa_visualizer
```
Install dependencies:
```sh
pip install -r requirements.txt
```

### Usage
Run the main script:
```sh
python main.py
```
Follow the prompts to enter a regex and view the NFA/DFA transitions and visualizations.

## Project Structure
```
core/
    nfa.py            # NFA construction and logic
    dfa.py            # DFA construction and logic
    regex_parser.py   # Regex parsing utilities
    visualizer.py     # Automata visualization (networkx/matplotlib)
main.py               # Entry point for CLI usage
requirements.txt      # Python dependencies
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
- Visualizes automata using networkx and matplotlib
- Prints automata states and transitions in readable format

## Contributing
Pull requests and suggestions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
MIT License

## Author
Akash Das
