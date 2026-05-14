# multi-agent-system

Implementation of the ReAct (Reason + Act) agent pattern from scratch

## How It Works

1. Claude **reasons** about what to do next (Thought)
2. Claude **acts** by choosing a tool (Action / Action Input)
3. You execute the tool and feed the result back (Observation)
4. Repeat until Claude has a final answer (FINISH)

## Tools

| Tool | Args | Description |
|---|---|---|
| `calculator` | Postfix expression (e.g. `42 47 *`) | Evaluates arithmetic using a stack |
| `read_file` | File path | Returns file contents |
| `write_file` | `path,content` | Writes content to file |

## Setup

```bash
pip install -r requirements.txt
```

```bash
cp .env.example .env # Fill in your API keys
```

## Usage

```bash
py -3.11 agent.py
```
Test prompt:
```
User: Read input.txt, multiply the number inside by 47, write the result to output.txt, then tell me what you wrote.
```

## Stack

- Python 3.11
- Anthropic SDK (`claude-haiku-4-5-20251001`)