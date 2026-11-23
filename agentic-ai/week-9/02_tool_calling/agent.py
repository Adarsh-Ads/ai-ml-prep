
import json
import os

from dotenv import load_dotenv
from google import genai

from tools import AVAILABLE_TOOLS


# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found. Check your .env file."
    )

MODEL = "gemini-3.5-flash-lite"

client = genai.Client(api_key=API_KEY)


# --------------------------------------------------
# 2. Tool definitions
#    These schemas tell Gemini what tools exist.
# --------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "name": "calculator",
        "description": (
            "Evaluate a mathematical expression. "
            "Use this for arithmetic calculations."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": (
                        "Mathematical expression, "
                        "for example: 75000 * 0.18"
                    ),
                }
            },
            "required": ["expression"],
        },
    },
    {
        "type": "function",
        "name": "text_statistics",
        "description": (
            "Calculate the character count, word count, "
            "and sentence count of a given text."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to analyze.",
                }
            },
            "required": ["text"],
        },
    },
    {
        "type": "function",
        "name": "get_current_datetime",
        "description": (
            "Get the current local date and time."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
]


# --------------------------------------------------
# 3. Agent execution loop
# --------------------------------------------------

def run_agent(user_query: str, max_iterations: int = 5):

    print("\nUser:", user_query)

    # Initial request to Gemini
    print("\nSending request to Gemini...", flush=True)

    interaction = client.interactions.create(
        model=MODEL,
        input=user_query,
        tools=TOOLS,
    )

    # ReAct-style loop:
    # Reason -> Act -> Observe -> Repeat

    for iteration in range(1, max_iterations + 1):

        print(f"\n--- Iteration {iteration} ---")

        function_calls = [
            step
            for step in (interaction.steps or [])
            if step.type == "function_call"
        ]

        # No more tool calls: agent has finished.
        if not function_calls:
            print("\nAgent:", interaction.output_text)
            return

        function_results = []

        # Execute every requested function call.
        for call in function_calls:

            tool_name = call.name
            arguments = call.arguments or {}

            print(f"\nTool requested: {tool_name}")
            print("Arguments:", arguments)

            # Security: only execute registered tools.
            if tool_name not in AVAILABLE_TOOLS:

                result = {
                    "error": f"Unknown tool: {tool_name}"
                }

            else:

                try:
                    tool_function = AVAILABLE_TOOLS[tool_name]

                    # Actual Python function execution
                    result = tool_function(**arguments)

                except Exception as error:
                    result = {
                        "error": str(error)
                    }

            print("Tool result:", result)

            function_results.append(
                {
                    "type": "function_result",
                    "name": tool_name,
                    "call_id": call.id,
                    "result": [
                        {
                            "type": "text",
                            "text": json.dumps(result, ensure_ascii=False),
                        }
                    ],
                }
            )

        # Send tool results back to Gemini.
        # Gemini uses these observations to decide what to do next.

        print("\nSending tool results back to Gemini...")

        interaction = client.interactions.create(
            model=MODEL,
            previous_interaction_id=interaction.id,
            input=function_results,
        )

    print(
        "\nMaximum iterations reached. "
        "Agent stopped to prevent an infinite loop."
    )


# --------------------------------------------------
# 4. Main entry point
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 50)
    print("       GEMINI TOOL-CALLING AGENT")
    print("=" * 50)

    query = input("\nEnter your query: ").strip()

    if query:
        try:
            run_agent(query)
        except Exception as error:
            print(f"\nAgent execution failed: {error}")
    else:
        print("Please enter a valid query.")

    client.close()
