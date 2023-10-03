from rich.tree import Tree
from rich.text import Text
from rich import print
import pathlib

from . import utils

def get_dir_contents(dir: pathlib.Path = pathlib.Path.cwd(), 
                     maximum_depth: int = 3) -> Tree:
    """Return a Tree containing the contents of a directory."""
    if not dir.exists():
        raise FileNotFoundError(f"Directory {dir} does not exist.")

    tree = Tree(
        # f":open_file_folder: [link file://{dir}]{dir}",
        f":open_file_folder: {dir}",
    )

    utils.walk_dir(dir, tree, ignore_files=False, ignore_dirs=False,
                   ignore_filetypes=False, search_depth=0, maximum_depth=maximum_depth)

    return tree

# Search for all files in directory and subdirectories that are a certain type
# (e.g. .py, .md, .txt, etc.)
def find_files_type(dir: pathlib.Path, 
                    file_types: list[str], 
                    search_depth: int, maximum_depth: int = 3,
                    absolute: bool = False,
                    search_full_path: bool = False) -> None:
    """Print all files of a certain type in a directory and subdirectories."""

    paths = pathlib.Path(dir).iterdir()

    for path in paths:
        if path.is_dir():
            if search_depth < maximum_depth and not search_full_path:
                find_files_type(path, file_types, search_depth + 1, 
                                maximum_depth, absolute, search_full_path)
            elif search_full_path:
                find_files_type(path, file_types, search_depth + 1, 
                                maximum_depth, absolute, search_full_path)
        elif path.is_file():
            if path.suffix in file_types:
                if absolute:
                    raw_txt = f"HIT: {path.parent}/{path.name}"
                else:
                    # Get file path relative to current working directory
                    raw_txt = f"HIT: {path.parent.relative_to(pathlib.Path.cwd())}" \
                    f"/{path.name}"

                print_txt = Text(raw_txt)
                # print_txt.highlight_words(file_types, "underline bold")
                # print_txt.highlight_words(f"{path.parent}/", "cyan")
                print_txt.stylize("cyan", 4, len(raw_txt) - len(path.name))
                print_txt.stylize("bold green", len(raw_txt) - len(path.name))

                print(print_txt)
    