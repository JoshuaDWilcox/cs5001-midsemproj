# Orchestral AI — Scientific Research Agent (Proof of Concept)

A proof-of-concept implementation based on the **Orchestral AI** paper ([arXiv:2601.02577](https://arxiv.org/pdf/2601.02577)), inspired by the **ASTER** (Agentic Science Toolkit for Exoplanet Research) use case described in Section 7.2.

This project demonstrates how the Orchestral AI framework can be used to build a **scientific research agent** with domain-specific tools for exoplanet analysis, statistical computation, and visualization — all running locally with **Ollama** (no API keys required).

## Features

- **Agent Architecture** — LLM + domain-specific tools + context orchestration
- **Provider-Agnostic Design** — Uses Ollama locally; swap to Claude/GPT/Gemini with one line
- **Custom Scientific Tools** — Exoplanet data retrieval, transit depth calculation, habitable zone estimation, statistical analysis, matplotlib plotting
- **Multi-Agent Collaboration** — Research Analyst vs Peer Reviewer scientific debate
- **Cost Tracking** — Automatic usage tracking across providers

## Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running
- At least one Ollama model pulled (e.g., `ollama pull llama3.2:3b`)

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/cs5001-midsemproj.git
cd cs5001-midsemproj
pip install -r requirements.txt
```

### Run the Research Workflow Demo

```bash
python research_demo.py
```

This runs a complete 8-step scientific research workflow:
1. Query the exoplanet catalog
2. Retrieve WASP-39b data
3. Compute transit depth
4. Estimate habitable zone
5. Perform statistical analysis (numpy)
6. Generate a visualization (matplotlib)
7. Save a research note
8. Agent-powered conversational analysis

### Run the Multi-Agent Demo

```bash
python multi_agent_demo.py
```

A **Research Analyst** and **Peer Reviewer** debate TRAPPIST-1e's habitability.

## Project Structure

```
cs5001-midsemproj/
├── research_demo.py       # 8-step scientific workflow demo
├── multi_agent_demo.py    # Multi-agent peer review discussion
├── custom_tools.py        # Domain-specific tools (@define_tool)
├── requirements.txt       # Python dependencies
├── report.md              # 1-page reflection report
├── README.md              # This file
├── screenshots/           # Screenshots of runs
└── workspace/             # Agent workspace (generated plots, notes)
```

## Key Concepts Demonstrated

| Concept | Implementation |
|---|---|
| Agent Architecture | `research_demo.py` — LLM + tools + system prompt |
| Provider-Agnostic | `Ollama(model=...)` swap to `Claude()`, `GPT()`, `Gemini()` |
| Tool Calling | `custom_tools.py` — 7 tools via `@define_tool()` decorator |
| Multi-Agent | `multi_agent_demo.py` — two agents in structured debate |
| Cost Tracking | `agent.get_total_cost()` — automatic per-agent tracking |
| Reproducibility | Research notes and plots saved to `workspace/` |

## Screenshots

### Research Workflow Demo
![Research Demo](screenshots/research_demo.png)

### Multi-Agent Scientific Discussion
![Multi-Agent Output](screenshots/multi_agent_output.png)

## Configuration

To switch LLM providers, change the model in any demo script:

```python
from orchestral.llm import Ollama, Claude, GPT, Gemini

# Local (free, no API key)
llm = Ollama(model="llama3.2:3b")

# Cloud providers (requires API key in .env)
# llm = Claude(model="claude-sonnet-4-0")
# llm = GPT(model="gpt-4o")
# llm = Gemini(model="gemini-2.0-flash-exp")
```

## References

- **Paper:** Orchestral AI: A Framework for Agent Orchestration ([arXiv:2601.02577](https://arxiv.org/pdf/2601.02577))
- **Framework:** [github.com/orchestralAI/orchestral-ai](https://github.com/orchestralAI/orchestral-ai)
- **ASTER Use Case:** Section 7.2 of the paper — Agentic Science Toolkit for Exoplanet Research