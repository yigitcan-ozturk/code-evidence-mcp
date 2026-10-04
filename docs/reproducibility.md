# Reproducibility fixture

This fixture gives MCP clients a deterministic two-language repository to inspect.

## Python

`tests/fixtures/chain.py` contains:

```text
handle_request → validate → persist
```

Expected query:

```text
explain_change_impact("tests/fixtures/chain.py:handle_request")
```

Expected evidence chain:

```text
handle_request calls validate
validate calls persist
```

## Go

`tests/fixtures/sample.go` contains:

```text
handleRequest → validate → persist
```

The important property is not natural-language similarity. Every reported edge must have a source location extracted from the repository.

## MCP Inspector

After installing the project:

```bash
npx @modelcontextprotocol/inspector code-evidence-mcp
```

1. Call `index_repository` with the repository root.
2. Call `explain_change_impact` with one of the fixture symbols above.
3. Verify that each impact contains `source`, `relation`, `target`, and `reason`.
4. Query a missing symbol and verify that no impact claim is returned.
