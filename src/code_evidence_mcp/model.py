from dataclasses import dataclass, field


@dataclass(frozen=True)
class Evidence:
    source: str
    relation: str
    target: str
    reason: str


@dataclass
class EvidenceGraph:
    edges: list[Evidence] = field(default_factory=list)

    def add(self, source: str, relation: str, target: str, reason: str) -> None:
        edge = Evidence(source, relation, target, reason)
        if edge not in self.edges:
            self.edges.append(edge)

    def impacts(self, symbol: str) -> list[Evidence]:
        """Return evidence whose source is directly or transitively reachable."""
        result: list[Evidence] = []
        frontier = [symbol]
        seen = {symbol}
        while frontier:
            current = frontier.pop(0)
            for edge in self.edges:
                if edge.source == current and edge not in result:
                    result.append(edge)
                    if edge.target not in seen:
                        seen.add(edge.target)
                        frontier.append(edge.target)
        return result
