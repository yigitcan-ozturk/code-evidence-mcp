# code-evidence-mcp

**Evidence-aware code context for AI coding agents.**

Code context can tell an agent what code exists. Code Evidence adds a deterministic answer to a different question:

> **What could this change affect — and what repository evidence supports that claim?**

Independent experiment inspired by John Crickett's Coding Challenge #139: Code Context MCP Server.

## v0.1

- MCP server over stdio
- deterministic Python symbol extraction
- function-call relationship graph
- transitive change-impact traversal
- evidence returned with every relationship
- tests for the evidence boundary

No LLM is used to invent dependency edges. If repository evidence does not establish a relationship, v0.1 does not claim it.

## Model

```text
Repository → Symbols → Relationships → Change → Impact → Evidence
```

Each edge records `source → relation → target` plus the repository location/reason supporting it.

## MCP tools

- `index_repository(path)` — indexes a local Python repository.
- `explain_change_impact(symbol)` — traverses downstream relationships and returns impacts plus evidence.

## Install

```bash
git clone https://github.com/yigitcan-ozturk/code-evidence-mcp.git
cd code-evidence-mcp
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
pytest
code-evidence-mcp
```

## Why evidence-aware?

Semantic similarity is useful for retrieval, but similarity is not proof of impact. Code Evidence keeps retrieval and evidence separate. The initial boundary is deliberately narrow and deterministic.

## Roadmap

- [x] deterministic Python symbol/call evidence
- [x] MCP surface
- [x] transitive impact explanation
- [ ] Tree-sitter multi-language parsing
- [ ] lexical + semantic/hybrid retrieval
- [ ] repository registration and persistence
- [ ] Git diff → changed-symbol mapping
- [ ] CODEOWNERS / OpenAPI / AsyncAPI evidence
- [ ] MCP Inspector reproducibility fixture

## Status

Experimental v0.1.
