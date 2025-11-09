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
import os
import configparser

init(autoreset=True)

# Load config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'mini_lex_config.ini')
config = configparser.ConfigParser(allow_no_value=True)
config.read(CONFIG_PATH)

# Load keywords
KEYWORDS = set()
if 'KEYWORDS' in config:
	for kw in config['KEYWORDS']:
		KEYWORDS.add(kw)

# Load token patterns
TOKEN_SPECIFICATION = []
if 'TOKENS' in config:
	for name, pattern in config['TOKENS'].items():
		TOKEN_SPECIFICATION.append((name, pattern))

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
		if kind == 'ID':
			if value in KEYWORDS:
				yield Token('KEYWORD', value, line_num)
			else:
				yield Token('ID', value, line_num)
		elif kind == 'ML_COMMENT':
			yield Token('ML_COMMENT', value, line_num)
			line_num += value.count('\n')
		elif kind == 'NEWLINE':
			line_num += 1
		elif kind == 'SKIP':
			pass
		elif kind == 'MISMATCH':
			print(f"[Error] Invalid token '{value}' at line {line_num}", file=sys.stderr)
			yield Token('INVALID', value, line_num)
		else:
			yield Token(kind, value, line_num)

def color_token(token):
	color_map = {
		'BLACK': Fore.BLACK,
		'RED': Fore.RED,
		'GREEN': Fore.GREEN,
		'YELLOW': Fore.YELLOW,
		'BLUE': Fore.BLUE,
		'MAGENTA': Fore.MAGENTA,
		'CYAN': Fore.CYAN,
		'WHITE': Fore.WHITE,
		'LIGHTBLACK_EX': Fore.LIGHTBLACK_EX,
		'LIGHTRED_EX': Fore.LIGHTRED_EX,
		'LIGHTGREEN_EX': Fore.LIGHTGREEN_EX,
		'LIGHTYELLOW_EX': Fore.LIGHTYELLOW_EX,
		'LIGHTBLUE_EX': Fore.LIGHTBLUE_EX,
		'LIGHTMAGENTA_EX': Fore.LIGHTMAGENTA_EX,
		'LIGHTCYAN_EX': Fore.LIGHTCYAN_EX,
		'LIGHTWHITE_EX': Fore.LIGHTWHITE_EX,
	}
	if 'COLORS' in config and token.type in config['COLORS']:
		config_color = config['COLORS'][token.type].upper()
		color = color_map.get(config_color, None)
		if color:
			return color + token.value + Style.RESET_ALL
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
