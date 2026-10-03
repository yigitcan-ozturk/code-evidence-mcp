from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .indexer import index_python

mcp = FastMCP("code-evidence")
_graph = None


@mcp.tool()
def index_repository(path: str) -> dict:
    """Index a local Python repository into an evidence graph."""
    global _graph
    root = Path(path).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Repository path does not exist: {root}")
    _graph = index_python(root)
    return {"repository": str(root), "evidence_edges": len(_graph.edges)}


@mcp.tool()
def explain_change_impact(symbol: str) -> dict:
    """Explain deterministic downstream impact and return supporting evidence."""
    if _graph is None:
        raise ValueError("No repository indexed. Call index_repository first.")
    edges = _graph.impacts(symbol)
    return {
        "symbol": symbol,
        "impact_count": len(edges),
        "evidence": [
            {
                "source": e.source,
                "relation": e.relation,
                "target": e.target,
                "reason": e.reason,
            }
            for e in edges
        ],
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
