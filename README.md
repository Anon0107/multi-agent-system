# multi-agent-system

ReAct (Reason + Act) agent built from scratch — no frameworks.

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
| `web_search` | Search query | Searches the web via Tavily |
| `get_weather` | City name | Returns weather data for a city |
| `search_news` | `query,country` | Searches news by query and country |
| `analyze_sentiment` | Text string | Analyzes sentiment of given text |
| `search_documents` | Search query | Queries local BanG Dream document database |

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

## Usage

```bash
py -3.11 agent.py
```

## Stack

- Python 3.11
- Anthropic SDK (`claude-haiku-4-5-20251001`)
- Tavily
- MCP