
import re

class LogicExpression:
    def __init__(self, expr: str):
        """Initialize with the expression string."""
        self.expr = expr
        self.tokens = None
        self.ast = None
        self._analyze()

    def _analyze(self):
        """Tokenize and parse the expression."""
        self.tokens = self.tokenize(self.expr)
        self.ast = self.parse(self.tokens)

    def tokenize(self, expr: str):
        """Convert expression string to tokens."""
        token_spec = r"\s*(and|or|not|\(|\)|[A-Za-z][A-Za-z0-9_]*)\s*"
        tokens = re.findall(token_spec, expr)
        return [t for t in tokens if t.strip()]

    def parse(self, tokens):
        """Build AST from tokens using recursive descent parsing with better error handling."""
        self._tokens = tokens
        self._pos = 0

        def peek():
            return self._tokens[self._pos] if self._pos < len(self._tokens) else None

        def consume():
            tok = peek()
            self._pos += 1
            return tok

        def parse_expr():
            return parse_or()

        def parse_or():
            left = parse_and()
            while peek() == 'or':
                op = consume()
                if peek() is None:
                    raise SyntaxError("Expression cannot end with 'or'")
                right = parse_and()
                left = (op, left, right)
            return left

        def parse_and():
            left = parse_not()
            while peek() == 'and':
                op = consume()
                if peek() is None:
                    raise SyntaxError("Expression cannot end with 'and'")
                right = parse_not()
                left = (op, left, right)
            return left

        def parse_not():
            if peek() == 'not':
                op = consume()
                if peek() is None:
                    raise SyntaxError("'not' must be followed by an expression")
                operand = parse_not()
                return (op, operand)
            else:
                return parse_atom()

        def parse_atom():
            tok = peek()
            if tok == '(': 
                consume()
                node = parse_expr()
                if peek() == ')':
                    consume()
                else:
                    raise SyntaxError('Expected closing parenthesis')
                return node
            elif tok is None:
                raise SyntaxError('Unexpected end of expression')
            elif re.match(r'^[A-Za-z][A-Za-z0-9_]*$', tok):
                return consume()
            else:
                raise SyntaxError(f'Unexpected token: {tok}')

        ast = parse_expr()
        if self._pos != len(self._tokens):
            raise SyntaxError('Unexpected tokens at end of expression')
        return ast

    def evaluate(self, var_values: dict):
        """Evaluate AST with given variable assignments."""
        def eval_node(node):
            if isinstance(node, str):
                # Variable
                if node not in var_values:
                    raise ValueError(f"Variable '{node}' not provided.")
                return bool(var_values[node])
            elif isinstance(node, tuple):
                if node[0] == 'not':
                    return not eval_node(node[1])
                elif node[0] == 'and':
                    return eval_node(node[1]) and eval_node(node[2])
                elif node[0] == 'or':
                    return eval_node(node[1]) or eval_node(node[2])
                else:
                    raise ValueError(f"Unknown operator: {node[0]}")
            else:
                raise ValueError(f"Invalid AST node: {node}")
        return eval_node(self.ast)

    def summary(self):
        """Return analysis summary (tokens, AST, variables, etc.)."""
        return {
            "original": self.expr,
            "tokens": self.tokens,
            "ast": self.ast,
            "variables": self.variables()
        }

    def variables(self):
        """Return list of variables in the expression."""
        return list(set(t for t in self.tokens if re.match(r"^[A-Za-z][A-Za-z0-9_]*$", t) and t not in {"and", "or", "not"}))

    def to_string(self):
        """Return a string representation of the AST or expression."""
        return str(self.ast)