from code_evidence_mcp.model import EvidenceGraph


def test_dependencies_follow_call_direction():
    graph = EvidenceGraph()
    graph.add("handler", "calls", "validate", "handler calls validate")
    graph.add("validate", "calls", "persist", "validate calls persist")
    assert [(e.source, e.target) for e in graph.dependencies("handler")] == [
        ("handler", "validate"),
        ("validate", "persist"),
    ]


def test_changed_callee_impacts_callers_transitively():
    graph = EvidenceGraph()
    graph.add("handler", "calls", "validate", "handler calls validate")
    graph.add("validate", "calls", "persist", "validate calls persist")
    assert [(e.source, e.target) for e in graph.impacts("persist")] == [
        ("validate", "persist"),
        ("handler", "validate"),
    ]


def test_unknown_symbol_produces_no_impact_claim():
    graph = EvidenceGraph()
    graph.add("a", "calls", "b", "a calls b")
    assert graph.impacts("missing") == []


def test_cycle_terminates_without_duplicate_evidence():
    graph = EvidenceGraph()
    graph.add("a", "calls", "b", "a calls b")
    graph.add("b", "calls", "a", "b calls a")
    impacts = graph.impacts("a")
    assert len(impacts) == 2
    assert len(set(impacts)) == 2
