
import ast
import operator
from datetime import datetime


# Tool 1: Calculator
def calculator(expression: str):
    """Evaluate a basic arithmetic expression."""

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            left = evaluate(node.left)
            right = evaluate(node.right)
            return allowed_operators[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and isinstance(
            node.op, (ast.USub, ast.UAdd)
        ):
            value = evaluate(node.operand)
            return -value if isinstance(node.op, ast.USub) else value

        raise ValueError("Unsupported expression")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree.body)


# Tool 2: Text statistics
def text_statistics(text: str):
    """Calculate basic statistics about a text."""

    words = text.split()

    return {
        "characters": len(text),
        "words": len(words),
        "sentences": sum(
            text.count(mark) for mark in [".", "!", "?"]
        )
    }


# Tool 3: Current date and time
def get_current_datetime():
    """Return the current local system date and time."""

    return datetime.now().astimezone().isoformat()


# Registry: Maps function names to Python functions
AVAILABLE_TOOLS = {
    "calculator": calculator,
    "text_statistics": text_statistics,
    "get_current_datetime": get_current_datetime,
}
