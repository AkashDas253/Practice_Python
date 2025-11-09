## Lexical Analyzer (Mini Lex)

**Goal:** Tokenize source code using regex & automata.
**Concepts:** Tokens, patterns, lexemes, finite automata.

### Features
- Define token types: keywords, identifiers, numbers, operators, punctuation, strings, chars, comments, whitespace
- Output: token stream with type, value, and line number
- Highlight invalid tokens (colored output)
- Real-time token coloring in terminal
- Handles comments and whitespace

### Usage
1. Place your source code in a file (e.g., `test.c`).
2. Run:
   ```
   python mini_lex.py test.c
   ```
3. See colored token output in terminal.

### Supported Tokens
- Keywords (e.g., `if`, `else`, `int`, ...)
- Identifiers
- Numbers (integers, floats)
- Operators (`+`, `-`, `*`, `/`, `=`, `==`, `!=`, etc.)
- Punctuation (`(`, `)`, `{`, `}`, `;`, `,`)
- Strings (e.g., "hello world")
- Character literals (e.g., 'a')
- Comments (`// ...`, `/* ... */`)
- Whitespace


### Requirements
- Python 3.x
- `colorama` library (exact version: 0.4.6)

Install dependencies:
```
pip install -r requirements.txt
```

### Sample Output
```
Line  Type       Value               
----------------------------------------
1     KEYWORD    int                 
1     ID         main                
1     PUNCT      (                   
1     PUNCT      )                   
1     PUNCT      {                   
...   ...        ...                 
```

### Extensibility
- Add more token types (e.g., preprocessor directives)
- Integrate with `ply.lex` for advanced lexing
- Improve error reporting
