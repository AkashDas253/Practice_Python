"""
Mini Lexical Analyzer (Mini Lex)

Goal: Tokenize source code using regex & automata.
Features:
- Define token types: keywords, identifiers, numbers, operators, comments, whitespace
- Output: token stream with type, value, and line number
- Highlight invalid tokens (colored output)
- Real-time token coloring in terminal

Usage:
    python mini_lex.py <source_file>
"""

import re
import sys
from colorama import Fore, Style, init

init(autoreset=True)

# Token specification
KEYWORDS = {
    'if', 'else', 'for', 'while', 'return', 'int', 'float', 'char', 'void', 'break', 'continue', 'switch', 'case', 'default', 'do', 'struct', 'typedef', 'enum', 'const', 'unsigned', 'signed', 'long', 'short', 'double', 'sizeof'
}
TOKEN_SPECIFICATION = [
    ('ML_COMMENT',  r'/\*[\s\S]*?\*/'),
    ('COMMENT',     r'//.*'),
    ('STRING',      r'"([^"\\]|\\.)*"'),
    ('CHAR',        r"'([^'\\]|\\.)'"),
    ('NUMBER',      r'\d+\.\d+|\d+'),
    ('ID',          r'[A-Za-z_]\w*'),
    ('OP',          r'(==|!=|<=|>=|\+\+|--|[+\-*/=<>!])'),
    ('PUNCT',       r'[(){};,]'),
    ('NEWLINE',     r'\n'),
    ('SKIP',        r'[ \t]+'),
    ('MISMATCH',    r'.'),
]

token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)

class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line
    def __repr__(self):
        return f"Token(type={self.type}, value={self.value}, line={self.line})"

def tokenize(code):
    line_num = 1
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            if '.' in value:
                yield Token('FLOAT', value, line_num)
            else:
                yield Token('INT', value, line_num)
        elif kind == 'ID':
            if value in KEYWORDS:
                yield Token('KEYWORD', value, line_num)
            else:
                yield Token('ID', value, line_num)
        elif kind == 'OP':
            yield Token('OP', value, line_num)
        elif kind == 'PUNCT':
            yield Token('PUNCT', value, line_num)
        elif kind == 'STRING':
            yield Token('STRING', value, line_num)
        elif kind == 'CHAR':
            yield Token('CHAR', value, line_num)
        elif kind == 'COMMENT':
            yield Token('COMMENT', value, line_num)
        elif kind == 'ML_COMMENT':
            yield Token('ML_COMMENT', value, line_num)
            line_num += value.count('\n')
        elif kind == 'NEWLINE':
            line_num += 1
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            yield Token('INVALID', value, line_num)

def color_token(token):
    if token.type == 'KEYWORD':
        return Fore.BLUE + token.value + Style.RESET_ALL
    elif token.type == 'ID':
        return Fore.GREEN + token.value + Style.RESET_ALL
    elif token.type == 'NUMBER':
        return Fore.CYAN + token.value + Style.RESET_ALL
    elif token.type == 'OP':
        return Fore.YELLOW + token.value + Style.RESET_ALL
    elif token.type == 'PUNCT':
        return Fore.WHITE + Style.BRIGHT + token.value + Style.RESET_ALL
    elif token.type == 'COMMENT' or token.type == 'ML_COMMENT':
        return Fore.MAGENTA + token.value + Style.RESET_ALL
    elif token.type == 'STRING':
        return Fore.LIGHTBLUE_EX + token.value + Style.RESET_ALL
    elif token.type == 'CHAR':
        return Fore.LIGHTCYAN_EX + token.value + Style.RESET_ALL
    elif token.type == 'INT':
        return Fore.CYAN + token.value + Style.RESET_ALL
    elif token.type == 'FLOAT':
        return Fore.LIGHTCYAN_EX + token.value + Style.RESET_ALL
    elif token.type == 'INVALID':
        return Fore.RED + Style.BRIGHT + token.value + Style.RESET_ALL
    else:
        return token.value

def main():
    if len(sys.argv) < 2:
        print("Usage: python mini_lex.py <source_file>")
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        code = f.read()
    print(f"{'Line':<5} {'Type':<10} {'Value':<20}")
    print('-'*40)
    for token in tokenize(code):
        print(f"{token.line:<5} {token.type:<10} {color_token(token):<20}")

if __name__ == "__main__":
    main()
