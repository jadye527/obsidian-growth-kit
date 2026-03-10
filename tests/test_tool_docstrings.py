import ast
from pathlib import Path


def test_public_functions_in_python_tools_have_docstrings(repo_root):
    tools_dir = repo_root / "tools"
    missing = []

    for tool_path in sorted(tools_dir.iterdir()):
        if not tool_path.is_file():
            continue

        source = tool_path.read_text()
        if not source.startswith("#!/usr/bin/env python3"):
            continue

        module = ast.parse(source, filename=str(tool_path))
        for node in module.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            if node.name.startswith("_"):
                continue
            if ast.get_docstring(node):
                continue
            missing.append(f"{tool_path.name}:{node.name}")

    assert missing == []
