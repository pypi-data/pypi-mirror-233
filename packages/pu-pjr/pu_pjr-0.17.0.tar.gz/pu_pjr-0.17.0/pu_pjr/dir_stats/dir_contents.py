from rich.tree import Tree
from rich.text import Text
from rich import print
import pathlib
import re

from . import utils

def get_dir_contents(dir: pathlib.Path = pathlib.Path.cwd(), 
                     maximum_depth: int = 3,
                     ignore_files: bool = False, ignore_dirs: bool = False,
                     ignore_filetypes: bool = False, 
                     ignore_hidden_dirs: bool = False) -> Tree:
    """Return a Tree containing the contents of a directory."""
    if not dir.exists():
        raise FileNotFoundError(f"Directory {dir} does not exist.")

    tree = Tree(
        # f":open_file_folder: [link file://{dir}]{dir}",
        f":open_file_folder: {dir}",
    )

    utils.walk_dir(dir, tree, ignore_files=ignore_files, ignore_dirs=ignore_dirs,
                   ignore_hidden_dirs=ignore_hidden_dirs,
                   ignore_filetypes=ignore_filetypes, search_depth=0, 
                   maximum_depth=maximum_depth)

    return tree

# Search for all files in directory and subdirectories that are a certain type
# (e.g. .py, .md, .txt, etc.)
def find_files_type(dir: pathlib.Path, 
                    file_types: list[str], 
                    search_depth: int, maximum_depth: int = 3,
                    absolute: bool = False,
                    search_full_path: bool = False,
                    ignore_hidden_dirs: bool = False) -> None:
    """Print all files of a certain type in a directory and subdirectories."""

    try:
        paths = pathlib.Path(dir).iterdir()
    except PermissionError as e:
        text = Text(f"PERMISSION ERROR. {e.filename}", style="red")
        print(text)
        return

    for path in paths:
        try:
            if path.is_dir():
                if search_depth < maximum_depth and not search_full_path and \
                    not (ignore_hidden_dirs and path.name.startswith(".")):
                    find_files_type(path, file_types, search_depth + 1, 
                                    maximum_depth, absolute, search_full_path, 
                                    ignore_hidden_dirs)
                elif search_full_path \
                    and not (ignore_hidden_dirs and path.name.startswith(".")):
                    find_files_type(path, file_types, search_depth + 1, 
                                    maximum_depth, absolute, search_full_path,
                                    ignore_hidden_dirs)
            elif path.is_file():
                if path.suffix in file_types:
                    if absolute:
                        raw_txt = f"HIT: {path.parent}/{path.name}"
                    else:
                        # Get file path relative to current working directory
                        raw_txt = f"HIT: {path.parent.relative_to(pathlib.Path.cwd())}"\
                        f"/{path.name}"

                    print_txt = Text(raw_txt)
                    # print_txt.highlight_words(file_types, "underline bold")
                    # print_txt.highlight_words(f"{path.parent}/", "cyan")
                    print_txt.stylize("cyan", 4, len(raw_txt) - len(path.name))
                    print_txt.stylize("bold green", len(raw_txt) - len(path.name))

                    print(print_txt)
        except PermissionError as e:
            text = Text(f"PERMISSION ERROR. {e.filename}", style="red")
            print(text)
            continue
                
# Find files using a regex expression
def find_files_expression(dir: pathlib.Path, 
                          expression: str, 
                          search_depth: int, maximum_depth: int = 3,
                          absolute: bool = False,
                          search_full_path: bool = False, 
                          ignore_hidden_dirs: bool = False) -> None:
    """Print all files of a certain type in a directory and subdirectories."""

    try:
        paths = pathlib.Path(dir).iterdir()
    except PermissionError as e:
        text = Text(f"PERMISSION ERROR. {e.filename}", style="red")
        print(text)
        return

    for path in paths:
        try:
            if path.is_dir():
                if search_depth < maximum_depth and not search_full_path and \
                    not (ignore_hidden_dirs and path.name.startswith(".")):
                    find_files_expression(path, expression, search_depth + 1, 
                                        maximum_depth, absolute, search_full_path)
                elif search_full_path \
                    and not (ignore_hidden_dirs and path.name.startswith(".")):
                    find_files_expression(path, expression, search_depth + 1, 
                                        maximum_depth, absolute, search_full_path)
            elif path.is_file():
                #Check that the file name matches the expression
                # print(path.name, expression)
                match = re.search(re.escape(expression), path.name)
                if match:
                    if absolute:
                        raw_txt = f"HIT: {path.parent}/{path.name}"
                    else:
                        # Get file path relative to current working directory
                        raw_txt = f"HIT: {path.parent.relative_to(pathlib.Path.cwd())}"\
                        f"/{path.name}"

                    print_txt = Text(raw_txt)
                    print_txt.stylize("cyan", 4, len(raw_txt) - len(path.name))
                    print_txt.stylize("green", len(raw_txt) - len(path.name))
                    print_txt.stylize("bold", len(raw_txt) - len(path.name) + 
                                      match.start(), 
                                      len(raw_txt) - len(path.name) + match.end())

                    print(print_txt)
        except PermissionError as e:
            text = Text(f"PERMISSION ERROR. {e.filename}", style="red")
            print(text)
            continue