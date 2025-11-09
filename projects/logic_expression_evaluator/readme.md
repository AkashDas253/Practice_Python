
# Logic Expression Evaluator

This project provides a command-line tool to parse and evaluate boolean logic expressions with variables.

## Features
- Supports operators: `and`, `or`, `not`, parentheses for grouping
- Parses expressions into an Abstract Syntax Tree (AST)
- Evaluates expressions given variable assignments
- Prints a summary of the analysis (tokens, AST, variables)
- Handles syntax errors with clear messages

## Usage

Run from the `logic_expression_evaluator` directory:

```powershell
python cli.py "(A and B) or not C" --vars "A=1,B=0,C=1"
```

### Arguments
- `EXPR`: The logic expression to evaluate (e.g., `(A and B) or not C`)
- `--vars`: Variable assignments as comma-separated pairs (e.g., `A=1,B=0,C=1`)

### Output
- Prints the result (`True` or `False`)
- Prints a summary of the parsed expression

### Error Handling
- If the expression is invalid (e.g., ends with an operator, missing parenthesis), a clear error message is shown.

Example error:
```
Error: Expression cannot end with 'and'
```

## Example

```
python cli.py "(A and B) or not C" --vars "A=1,B=0,C=1"
Result: False
Summary:
	Original: (A and B) or not C
	Tokens: ['(', 'A', 'and', 'B', ')', 'or', 'not', 'C']
	AST: ('or', ('and', 'A', 'B'), ('not', 'C'))
	Variables: ['B', 'A', 'C']
```
