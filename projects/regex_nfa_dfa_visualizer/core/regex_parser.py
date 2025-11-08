"""
regex_parser.py
Utility functions and classes for parsing regular expressions.
"""

class RegexParser:
    def __init__(self, pattern: str):
        self.pattern = pattern

    def parse(self):
        """Convert infix regex to postfix (Shunting Yard algorithm)."""
        precedence = {'*': 3, '.': 2, '|': 1}
        output = []
        stack = []
        pattern = self._add_concat(self.pattern)
        for c in pattern:
            if c.isalnum():
                output.append(c)
            elif c == '(': 
                stack.append(c)
            elif c == ')':
                while stack and stack[-1] != '(': output.append(stack.pop())
                stack.pop()
            else:
                while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence.get(c, 0):
                    output.append(stack.pop())
                stack.append(c)
        while stack: output.append(stack.pop())
        return ''.join(output)

    def _add_concat(self, pattern):
        """Add explicit concatenation operator '.' to regex pattern."""
        result = ''
        for i, c in enumerate(pattern):
            result += c
            if i+1 < len(pattern):
                d = pattern[i+1]
                if (c.isalnum() or c == ')' or c == '*') and (d.isalnum() or d == '('):
                    result += '.'
        return result
