
import ast
import operator


# --------------------------------
# 1. TOOL IMPLEMENTATION
# --------------------------------

def calculator(expression: str):
    """Safely evaluate basic arithmetic expressions."""

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            left = evaluate(node.left)
            right = evaluate(node.right)
            return operators[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and isinstance(
            node.op, (ast.UAdd, ast.USub)
        ):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value

        raise ValueError("Unsupported mathematical expression")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree.body)


# --------------------------------
# 2. TOOL REGISTRY
# --------------------------------

tools = {
    "calculator": calculator
}


# --------------------------------
# 3. SIMULATED LLM
# --------------------------------

def mock_llm(user_input, observation=None):

    if observation is not None:
        return {
            "type": "final",
            "content": f"The calculation result is {observation}."
        }

    if user_input.lower().startswith("calculate "):
        expression = user_input[10:]

        return {
            "type": "tool_call",
            "tool": "calculator",
            "arguments": expression
        }

    return {
        "type": "final",
        "content": "I can answer simple questions, but I need a calculator tool for calculations."
    }


# --------------------------------
# 4. AGENT EXECUTION LOOP
# --------------------------------

def run_agent(user_input):

    observation = None

    for step in range(5):

        print(f"\n--- Agent Step {step + 1} ---")

        response = mock_llm(user_input, observation)

        if response["type"] == "final":
            print("Final Answer:", response["content"])
            return response["content"]

        if response["type"] == "tool_call":

            tool_name = response["tool"]
            arguments = response["arguments"]

            print("Selected Tool:", tool_name)
            print("Tool Input:", arguments)

            tool = tools[tool_name]
            observation = tool(arguments)

            print("Tool Observation:", observation)

    return "Maximum iterations reached."


# --------------------------------
# 5. RUN AGENT
# --------------------------------

if __name__ == "__main__":

    query = "calculate 25 * 80000 / 100"

    print("User:", query)

    run_agent(query)
