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

    def dependencies(self, symbol: str) -> list[Evidence]:
        """Return evidence for symbols this symbol directly/transitively depends on."""
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

    def impacts(self, symbol: str) -> list[Evidence]:
        """Return evidence for callers directly/transitively affected by a changed symbol."""
        result: list[Evidence] = []
        frontier = [symbol]
        seen = {symbol}
        while frontier:
            current = frontier.pop(0)
            for edge in self.edges:
                if edge.target == current and edge not in result:
                    result.append(edge)
                    if edge.source not in seen:
                        seen.add(edge.source)
                        frontier.append(edge.source)
        return result
