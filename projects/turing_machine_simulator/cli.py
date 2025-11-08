"""
Flexible Turing Machine CLI.
"""

from core.turing_machine import TuringMachine

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run a Turing Machine simulation.")
    parser.add_argument('--tape', type=str, default="1011", help="Initial tape input")
    parser.add_argument('--verbose', action='store_true', help="Show step-by-step output")
    args = parser.parse_args()

    tm_def = {
        'tape': args.tape,
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
    result = tm.run(verbose=args.verbose)
    print("Resulting tape:", result)

if __name__ == "__main__":
    main()
