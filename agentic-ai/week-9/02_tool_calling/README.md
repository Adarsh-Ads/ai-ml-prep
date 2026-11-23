# Week 9 — Day 2: LLM Tool Calling

## 1. Learning Objectives

By the end of this module, I implemented a real LLM-powered tool-calling agent using Google's Gemini API and Python.

The key objectives were:

- Understand how LLMs use external tools.
- Define Python functions that an LLM can call.
- Expose tools to Gemini using function declarations.
- Allow Gemini to select tools based on a user's request.
- Execute the selected functions in Python.
- Return tool results to Gemini.
- Handle multiple tool calls in a single interaction.
- Understand the tool-calling execution loop.

---

## 2. What Is Tool Calling?

Tool calling is a capability that allows an LLM to request the execution of external functions when it needs information or capabilities beyond generating text.

An LLM does not directly execute our Python functions. Instead, it identifies a suitable tool, generates a function call with arguments, and returns that request to our application.

Our Python application executes the function and sends the result back to the LLM.

The LLM can then use the result to generate a final response.

### Example

User:

`Calculate 18% of 75000.`

Gemini determines that it should use the calculator tool and requests:

```python
calculator(expression="75000 * 0.18")
```

Python executes the function and returns:

```text
13500.0
```

Gemini receives the result and responds:

`18% of 75,000 is 13,500.`

### Important distinction

The LLM decides which tool to call and what arguments to provide. The application is responsible for executing the function.

This separation is fundamental to tool-calling architecture.

---

## 3. Why Do LLMs Need Tools?

An LLM primarily generates responses based on its learned knowledge and the context provided to it.

However, many tasks require capabilities that are better handled by external systems.

Examples:

| Requirement | Suitable tool |
|---|---|
| Mathematical calculations | Python calculator |
| Current date and time | Date/time function |
| Database information | Database query |
| Live information | External API |
| File operations | Python file-processing function |
| Sending notifications | Email or messaging API |

Tools extend an LLM's capabilities by allowing it to interact with external systems.

---

## 4. Architecture

The tool-calling workflow implemented in this module:

```text
             User Query
                 |
                 v
          Python Application
                 |
                 v
             Gemini LLM
                 |
                 v
         Selects a Suitable Tool
                 |
                 v
          Function Call Request
                 |
                 v
          Python Tool Execution
                 |
                 v
             Tool Result
                 |
                 v
          Return Result to LLM
                 |
                 v
           Gemini Processes
             the Result
                 |
                 v
            Final Answer
```

The application manages the execution cycle.

The LLM decides what action is required, while Python performs the actual operation.

---

## 5. Project Structure

```text
agentic-ai/
│
├── week-9/
│   ├── 01_agent_fundamentals/
│   │
│   └── 02_tool_calling/
│       ├── tools.py
│       ├── agent.py
│       ├── test_gemini.py
│       └── README.md
│
├── .env
├── .env.example
├── .gitignore
└── requirements.txt
```

### File responsibilities

| File | Responsibility |
|---|---|
| `tools.py` | Defines Python functions and the available tools registry |
| `agent.py` | Connects to Gemini and manages the tool-calling loop |
| `test_gemini.py` | Tests Gemini API connectivity |
| `.env` | Stores the API key locally |
| `.env.example` | Provides an environment-variable template |
| `requirements.txt` | Lists project dependencies |

---

## 6. Environment Setup

### Dependencies

The implementation uses:

- `google-genai` — Google's Gen AI Python SDK.
- `python-dotenv` — Loads environment variables from `.env`.
- Python standard library — Used for JSON serialization, date/time operations, and other utility functions.

Install dependencies:

```powershell
pip install google-genai python-dotenv
```

LangGraph is not required for this module.

### API key configuration

Create a `.env` file in the `agentic-ai` directory:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

The API key is loaded using `python-dotenv`.

**Security:** Never commit `.env` or expose API keys in source code, screenshots, or public repositories.

### Model selection

The working model used in this implementation:

```python
MODEL = "gemini-3.5