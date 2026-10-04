from pathlib import Path
from code_evidence_mcp.indexer import index_repository

def test_go_call_evidence(tmp_path: Path):
    (tmp_path / "main.go").write_text(
        "package main\n\nfunc target() int { return 1 }\n\nfunc caller() int { return target() }\n",
        encoding="utf-8",
    )
    graph = index_repository(tmp_path)
    impacts = graph.dependencies("main.go:caller")
    assert len(impacts) == 1
    assert impacts[0].target == "main.go:target"
    assert impacts[0].reason.endswith("calls target")
