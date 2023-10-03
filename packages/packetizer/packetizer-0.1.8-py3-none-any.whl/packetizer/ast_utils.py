import ast


def get_used_names_or_alias(content):
    tree = ast.parse(content)
    used_names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    return used_names
