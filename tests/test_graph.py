from code_evidence_mcp.model import EvidenceGraph

def test_transitive_impact_is_evidence_backed():
    graph = EvidenceGraph()
    graph.add("a", "calls", "b", "a:1 calls b")
    graph.add("b", "calls", "c", "b:1 calls c")
    impacts = graph.impacts("a")
    assert [(e.source, e.target) for e in impacts] == [("a", "b"), ("b", "c")]

def test_unknown_symbol_produces_no_claim():
    graph = EvidenceGraph()
    graph.add("a", "calls", "b", "a:1 calls b")
    assert graph.impacts("missing") == []
