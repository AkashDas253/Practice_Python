## Turing Machine Simulator


# Turing Machine Simulator

## Goal
Simulate computation and undecidability using a flexible Turing machine implementation.

## Concepts
- Turing machine
- Tape
- State transitions
- Halting

## Features
- Input transition table via code or CLI
- Show tape movement, head position, and step tracing (verbose mode)
- Easily define custom Turing machines

## Usage

### CLI
Run a Turing machine from the command line:

```powershell
python cli.py --tape 1011 --verbose
```

### Python API
Import and use the class in your own code:

```python
from core.turing_machine import TuringMachine

tm_def = {
    'tape': "1011",
    'blank_symbol': "_",
    'initial_state': "start",
    'final_states': ["halt"],
    'transitions': {
        ("start", "0"): ("start", "0", "R"),
        ("start", "1"): ("start", "1", "R"),
        ("start", "_" ): ("inc", "_", "L"),
        ("inc", "0"): ("halt", "1", "N"),
        ("inc", "1"): ("inc", "0", "L"),
        ("inc", "_" ): ("halt", "1", "N"),
    }
}
tm = TuringMachine(tm_def)
result = tm.run(verbose=True)
print("Resulting tape:", result)
```

## Testing
Run unit tests:

```powershell
python test.py
```

## Extras
- Add “universal TM” that runs encoded TMs
- Animated tape head; optional web GUI (`streamlit` or `pygame`)
