from pathlib import Path

from code_evidence_mcp.indexer import index_repository


def test_deterministic_call_evidence(tmp_path: Path):
    (tmp_path / "sample.py").write_text(
        "def target():\n    return 1\n\ndef caller():\n    return target()\n",
        encoding="utf-8",
    )
    graph = index_repository(tmp_path)
    impacts = graph.impacts("sample.py:caller")
    assert len(impacts) == 1
    assert impacts[0].target == "sample.py:target"
    assert impacts[0].relation == "calls"
    assert impacts[0].reason == "sample.py:5 calls target"


def test_python_attribute_call_resolves_known_symbol(tmp_path: Path):
    (tmp_path / "sample.py").write_text(
        "class Service:\n    def target(self):\n        return 1\n\ndef caller(service):\n    return service.target()\n",
        encoding="utf-8",
    )
    graph = index_repository(tmp_path)
    impacts = graph.impacts("sample.py:caller")
    assert len(impacts) == 1
    assert impacts[0].target == "sample.py:target"
