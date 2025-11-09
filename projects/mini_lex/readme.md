## Lexical Analyzer (Mini Lex)

**Goal:** Tokenize source code using regex & automata.
**Concepts:** Tokens, patterns, lexemes, finite automata.

### Features
## Lexical Analyzer (Mini Lex)

**Goal:** Tokenize source code using regex & automata, with fully configurable tokens and colors.

### Features
- Define token types, keywords, and colors in `mini_lex_config.ini`
- Output: token stream with type, value, and line number
- Highlight invalid tokens (colored output)
- Real-time token coloring in terminal (colors set in config)
- Handles comments and whitespace

### Usage
1. Place your source code in a file (e.g., `test.c`).
2. Run:
    ```
    python mini_lex.py test.c
    ```
3. See colored token output in terminal.

### Configuration
- **Keywords:** List in `[KEYWORDS]` section of `mini_lex_config.ini`
- **Token Patterns:** Define regex for each token type in `[TOKENS]`
- **Colors:** Assign colors to token types in `[COLORS]` (see colorama docs for options)

### Testing
- Test with a correct file:
   ```
   python mini_lex.py test.c
   ```
- Test with an error file:
   ```
   python mini_lex.py test_error.c
   ```

### Requirements
- Python 3.x
- `colorama` library (exact version: 0.4.6)

Install dependencies:
```
pip install -r requirements.txt
```

### Extensibility
- Add or change token types, keywords, and colors in the config file
- Supports any language by editing config

---

Created by AkashDas253
- Improve error reporting
