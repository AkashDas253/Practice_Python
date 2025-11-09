"""
CLI for Logic Expression Evaluator
Usage:
    python cli.py "EXPR" --vars "A=1,B=0,C=1"
Example:
    python cli.py "(A and B) or not C" --vars "A=1,B=0,C=1"
"""
import argparse
from core import LogicExpression

def parse_vars(vars_str):
    vars = {}
    for item in vars_str.split(","):
        if "=" in item:
            k, v = item.split("=")
            vars[k.strip()] = bool(int(v.strip()))
    return vars

def print_summary(summary):
    print("Summary:")
    print(f"  Original: {summary['original']}")
    print(f"  Tokens: {summary['tokens']}")
    print(f"  AST: {summary['ast']}")
    print(f"  Variables: {summary['variables']}")

def main():
    parser = argparse.ArgumentParser(description="Logic Expression Evaluator CLI")
    parser.add_argument("expr", type=str, help="Logic expression to evaluate")
    parser.add_argument("--vars", type=str, default="", help="Variable assignments, e.g. A=1,B=0")
    args = parser.parse_args()

    expr = args.expr
    vars_dict = parse_vars(args.vars)

    try:
        logic_expr = LogicExpression(expr)
        result = logic_expr.evaluate(vars_dict)
        print(f"Result: {result}")
        print_summary(logic_expr.summary())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()