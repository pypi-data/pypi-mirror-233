import ast
from dataclasses import dataclass


@dataclass
class NameDto:
    name: str
    alias: str | None


@dataclass
class ImportDto:
    module: str
    alias: str | None
    names: list[NameDto] | None


class ClassExtractor(ast.NodeVisitor):
    def __init__(self):
        self.classes = {}
        self.imports = []

    def visit_Import(self, node: ast.Import):
        for n in node.names:
            import_dto = ImportDto(module=n.name, alias=n.asname, names=[])
            self.imports.append(import_dto)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = node.module
        node_names = []
        for n in node.names:
            node_names.append(NameDto(name=n.name, alias=n.asname))
        import_dto = ImportDto(module=module, alias=None, names=node_names)
        self.imports.append(import_dto)

    def visit_ClassDef(self, node: ast.ClassDef):
        source_lines = ast.unparse(node).split("\n")
        self.classes[node.name] = "\n".join(source_lines)
