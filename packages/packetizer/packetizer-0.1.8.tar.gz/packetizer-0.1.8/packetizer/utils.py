import os
import re

import typer


def convert_camel_case_to_snake_case(name):
    # Insert underscores before uppercase letters followed by lowercase letters
    _name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    # Insert underscores between lowercase or digit and uppercase letters
    _name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", _name).lower()
    return _name


def assert_file_exist(file_path):
    if not os.path.exists(file_path):
        typer.echo(f"Error: The file: ({file_path}) not found.")
        raise typer.Exit(code=1)


def assert_file_is_python_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension != ".py":
        typer.echo(f"Error: The file: ({file_path}) is not a Python file.")
        raise typer.Exit(code=1)
