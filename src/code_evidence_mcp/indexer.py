import ast
from pathlib import Path

from .model import EvidenceGraph


def index_python(root: Path) -> EvidenceGraph:
    """Build a deterministic symbol/call evidence graph from Python source."""
    graph = EvidenceGraph()
    definitions: dict[str, str] = {}
    parsed: list[tuple[Path, ast.AST]] = []

    for path in sorted(root.rglob("*.py")):
        if any(part.startswith(".") for part in path.parts):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        parsed.append((path, tree))
        rel = path.relative_to(root).as_posix()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                definitions.setdefault(node.name, f"{rel}:{node.name}")

    for path, tree in parsed:
        rel = path.relative_to(root).as_posix()
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            caller = f"{rel}:{node.name}"
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    name = _call_name(child.func)
                    if name and name in definitions:
                        graph.add(
                            caller,
                            "calls",
                            definitions[name],
                            f"{rel}:{getattr(child, 'lineno', '?')} calls {name}",
                        )
    return graph


def _call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None
