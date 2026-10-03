from pathlib import Path

from code_evidence_mcp.indexer import index_python


def test_deterministic_call_evidence(tmp_path: Path):
    (tmp_path / "sample.py").write_text(
        "def target():\n    return 1\n\ndef caller():\n    return target()\n",
        encoding="utf-8",
    )
    graph = index_python(tmp_path)
    impacts = graph.impacts("sample.py:caller")
    assert len(impacts) == 1
    assert impacts[0].target == "sample.py:target"
    assert impacts[0].relation == "calls"
    assert "calls target" in impacts[0].reason
