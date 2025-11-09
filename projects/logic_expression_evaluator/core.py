
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
        """Convert expression string to tokens, including all supported operators and aliases."""
        # Recognize all operators and aliases
        token_spec = r"\s*(<=>|=>|nand|nor|iff|and|or|not|xor|!|`|&|\||\^|\(|\)|[A-Za-z][A-Za-z0-9_]*)\s*"
        tokens = re.findall(token_spec, expr)
        return [t for t in tokens if t.strip()]

    def parse(self, tokens):
        """Build AST from tokens using recursive descent parsing with all supported operators and aliases."""
        self._tokens = tokens
        self._pos = 0

        def peek():
            return self._tokens[self._pos] if self._pos < len(self._tokens) else None

        def consume():
            tok = peek()
            self._pos += 1
            return tok

        # Operator precedence: implies (<=>, iff, =>) < or (or, nor, |) < xor (xor, ^) < and (and, nand, &) < not (not, !, `)
        def parse_expr():
            return parse_equiv()

        def parse_equiv():
            left = parse_implies()
            while peek() in {'<=>', 'iff'}:
                op = consume()
                if peek() is None:
                    raise SyntaxError("Expression cannot end with 'iff' or '<=>'")
                right = parse_implies()
                left = (op, left, right)
            return left

        def parse_implies():
            left = parse_or()
            while peek() == '=>':
                op = consume()
                if peek() is None:
                    raise SyntaxError("Expression cannot end with '=>' (implies)")
                right = parse_or()
                left = (op, left, right)
            return left

        def parse_or():
            left = parse_xor()
            while peek() in {'or', 'nor', '|'}:
                op = consume()
                if peek() is None:
                    raise SyntaxError("Expression cannot end with 'or', 'nor', or '|' (or)")
                right = parse_xor()
                left = (op, left, right)
            return left

        def parse_xor():
            left = parse_and()
            while peek() in {'xor', '^'}:
                op = consume()
                if peek() is None:
                    raise SyntaxError("Expression cannot end with 'xor' or '^' (xor)")
                right = parse_and()
                left = (op, left, right)
            return left

        def parse_and():
            left = parse_not()
            while peek() in {'and', 'nand', '&'}:
                op = consume()
                if peek() is None:
                    raise SyntaxError("Expression cannot end with 'and', 'nand', or '&' (and)")
                right = parse_not()
                left = (op, left, right)
            return left

        def parse_not():
            if peek() in {'not', '!', '`'}:
                op = consume()
                if peek() is None:
                    raise SyntaxError("'not', '!', or '`' must be followed by an expression")
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
        """Evaluate AST with given variable assignments, supporting all operators and aliases."""
        def eval_node(node):
            if isinstance(node, str):
                # Variable
                if node not in var_values:
                    raise ValueError(f"Variable '{node}' not provided.")
                return bool(var_values[node])
            elif isinstance(node, tuple):
                op = node[0]
                if op in {'not', '!', '`'}:
                    return not eval_node(node[1])
                elif op in {'and', '&'}:
                    return eval_node(node[1]) and eval_node(node[2])
                elif op == 'nand':
                    return not (eval_node(node[1]) and eval_node(node[2]))
                elif op in {'or', '|'}:
                    return eval_node(node[1]) or eval_node(node[2])
                elif op == 'nor':
                    return not (eval_node(node[1]) or eval_node(node[2]))
                elif op in {'xor', '^'}:
                    return eval_node(node[1]) != eval_node(node[2])
                elif op in {'=>'}:
                    # implies: A => B is (not A) or B
                    return (not eval_node(node[1])) or eval_node(node[2])
                elif op in {'iff', '<=>'}:
                    # equivalence: A iff B is (A and B) or (not A and not B)
                    return (eval_node(node[1]) and eval_node(node[2])) or (not eval_node(node[1]) and not eval_node(node[2]))
                else:
                    raise ValueError(f"Unknown operator: {op}")
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
        """Return list of variables in the expression, excluding all operators and aliases."""
        operators = {"and", "or", "not", "xor", "nand", "nor", "iff", "=>", "<=>", "!", "`", "&", "|", "^"}
        return list(set(t for t in self.tokens if re.match(r"^[A-Za-z][A-Za-z0-9_]*$", t) and t not in operators))

    def to_string(self):
        """Return a string representation of the AST or expression."""
        return str(self.ast)