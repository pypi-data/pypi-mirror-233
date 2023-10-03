import os

from packetizer.ast_utils import get_used_names_or_alias
from packetizer.utils import convert_camel_case_to_snake_case


def get_import_statements(imports, used_names: set) -> str:
    import_statements = ""
    for imp in imports:
        if imp.names:
            import_statement = f"from {imp.module} import "
            for name in imp.names:
                if name.alias and name.alias in used_names:
                    import_statement += f"{name.name} as {name.alias}, "

                elif name.alias is None and name.name in used_names:
                    import_statement += f"{name.name}, "

            if import_statement != f"from {imp.module} import ":
                import_statements += f"{import_statement[:-2]}\n"

        else:
            if imp.alias and imp.alias in used_names:
                import_statements += f"import {imp.module} as  {imp.alias}\n"

            elif imp.alias is None and imp.module in used_names:
                import_statements += f"import {imp.module}\n"

    return import_statements


def write_class_files(classes, imports, output_dir, suffix):
    for class_name, class_content in classes.items():
        file_name = convert_camel_case_to_snake_case(class_name)

        if suffix:
            file_name = f"{file_name}_{suffix}"

        file_path = f"{output_dir}/{file_name}.py"

        with open(file_path, "w") as f:
            used_names = get_used_names_or_alias(class_content)
            import_statements = get_import_statements(imports, used_names)

            f.write(import_statements)
            f.write("\n")
            f.write(f"\n{class_content}\n")
            f.write("\n")


def write_init_file(class_dict, output_dir):
    with open(f"{output_dir}/__init__.py", "w") as f:
        for class_name in class_dict.keys():
            file_name = convert_camel_case_to_snake_case(class_name)
            f.write(f"from .{file_name} import {class_name}\n")


def write_to_files(class_dict, imports, output_dir, suffix):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    write_class_files(classes=class_dict, imports=imports, output_dir=output_dir, suffix=suffix)

    write_init_file(class_dict, output_dir)
