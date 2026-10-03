from pathlib import Path

from tree_sitter import Language, Parser
import tree_sitter_go
import tree_sitter_python

from .model import EvidenceGraph

_LANGUAGES = {
    ".py": Language(tree_sitter_python.language()),
    ".go": Language(tree_sitter_go.language()),
}

_FUNCTION_TYPES = {
    ".py": {"function_definition"},
    ".go": {"function_declaration", "method_declaration"},
}

_CALL_TYPES = {
    ".py": {"call"},
    ".go": {"call_expression"},
}


def index_repository(root: Path) -> EvidenceGraph:
    """Build deterministic function/call evidence for supported languages."""
    graph = EvidenceGraph()
    definitions: dict[str, str] = {}
    parsed: list[tuple[Path, object, bytes]] = []

    for path in sorted(p for p in root.rglob("*") if p.suffix in _LANGUAGES):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        source = path.read_bytes()
        parser = Parser(_LANGUAGES[path.suffix])
        tree = parser.parse(source)
        parsed.append((path, tree.root_node, source))
        rel = path.relative_to(root).as_posix()
        for node in _walk(tree.root_node):
            if node.type in _FUNCTION_TYPES[path.suffix]:
                name = node.child_by_field_name("name")
                if name:
                    symbol = _text(name, source)
                    definitions.setdefault(symbol, f"{rel}:{symbol}")

    for path, root_node, source in parsed:
        rel = path.relative_to(root).as_posix()
        for fn in _walk(root_node):
            if fn.type not in _FUNCTION_TYPES[path.suffix]:
                continue
            name = fn.child_by_field_name("name")
            if not name:
                continue
            caller_name = _text(name, source)
            caller = f"{rel}:{caller_name}"
            for node in _walk(fn):
                if node.type not in _CALL_TYPES[path.suffix]:
                    continue
                target = _call_target(node, source)
                if target and target in definitions:
                    graph.add(
                        caller,
                        "calls",
                        definitions[target],
                        f"{rel}:{node.start_point.row + 1} calls {target}",
                    )
    return graph


def index_python(root: Path) -> EvidenceGraph:
    """Backward-compatible entry point; indexes all supported source files."""
    return index_repository(root)


def _walk(node):
    yield node
    for child in node.children:
        yield from _walk(child)


def _text(node, source: bytes) -> str:
    return source[node.start_byte:node.end_byte].decode("utf-8")


def _call_target(node, source: bytes) -> str | None:
    function = node.child_by_field_name("function")
    if function is None:
        # Python grammar exposes the called expression as the first named child.
        function = next((c for c in node.named_children if c.type not in {"argument_list"}), None)
    if function is None:
        return None
    if function.type in {"identifier"}:
        return _text(function, source)
    if function.type in {"attribute", "selector_expression"}:
        attr = function.child_by_field_name("attribute") or function.child_by_field_name("field")
        if attr:
            return _text(attr, source)
    return None
