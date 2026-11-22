
# Agent Fundamentals

## 1. What is an AI Agent?

An AI agent is a system that uses an LLM to make
decisions, interact with tools, observe results,
and perform actions toward a defined objective.

## 2. LLM Application vs RAG vs Agent

- LLM: Generates responses.
- RAG: Retrieves external information to augment
  LLM responses.
- Agent: Selects and executes actions to achieve goals.

## 3. Core Components

- LLM: Decision-making engine.
- Instructions: Defines objectives and constraints.
- Tools: External functions the agent can execute.
- State: Tracks current execution information.
- Memory: Retains useful information.
- Control Flow: Determines the next operation.
- Observation: Captures tool execution results.

## 4. ReAct Pattern

ReAct = Reason + Act.

Basic cycle:
1. Reason
2. Act
3. Observe
4. Repeat or Finish

## 5. Agent Execution Loop

User Input
    ↓
LLM Decision
    ↓
Tool Selection
    ↓
Tool Execution
    ↓
Observation
    ↓
LLM Decision
    ↓
Final Response

## 6. Practical Implementation

Implemented:
- Custom calculator tool
- Tool registry
- Simulated LLM
- Tool execution loop
- Observation handling
- Iteration limit

Next:
Replace simulated LLM with a real LLM
and implement genuine tool calling.
