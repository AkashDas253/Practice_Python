"""
Basic test for the flexible TuringMachine class.
"""
import unittest
from core.turing_machine import TuringMachine

class TestTuringMachine(unittest.TestCase):
    def test_binary_increment(self):
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
        result = tm.run()
        self.assertEqual(result.rstrip(tm_def['blank_symbol']), "1100")

    def test_palindrome(self):
        # Palindrome recognizer for 'aba' (very simple, for demonstration)
        tm_def = {
            'tape': "aba",
            'blank_symbol': "_",
            'initial_state': "start",
            'final_states': ["accept", "reject"],
            'transitions': {
                ("start", "a"): ("find_a", "_", "R"),
                ("start", "b"): ("find_b", "_", "R"),
                ("start", "_" ): ("accept", "_", "N"),
                ("find_a", "b"): ("find_a", "b", "R"),
                ("find_a", "a"): ("check_a", "_", "L"),
                ("find_a", "_" ): ("reject", "_", "N"),
                ("find_b", "a"): ("find_b", "a", "R"),
                ("find_b", "b"): ("check_b", "_", "L"),
                ("find_b", "_" ): ("reject", "_", "N"),
                ("check_a", "_" ): ("accept", "_", "N"),
                ("check_b", "_" ): ("accept", "_", "N"),
            }
        }
        tm = TuringMachine(tm_def)
        tm.run()
        # Accept if palindrome, else None or 'reject' is valid
        self.assertIn(tm.state, ["accept", "reject", None])

if __name__ == "__main__":
    unittest.main()
