import os
import pathlib

from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.tree import Tree

IGNORED_DIRS = (".git", ".venv", "__pycache__", "node_modules")
IGNORED_FILES = (".DS_Store", ".gitignore", ".python-version", 
                 "__init__.py", "__main__.py")
IGNORE_FILETYPES = (".ignore")

def folder_emoji(dir_path: pathlib.Path) -> str:
    """Return the emoji for a directory."""
    # if dir_path.name == ".git":
    #     return "🐙"
    # elif dir_path.name == ".venv":
    #     return "🐍"
    # elif dir_path.name == "__pycache__":
    #     return "🐍"
    # elif dir_path.name == "node_modules":
    #     return "📦"
    # else:
    try:
        contents = os.listdir(dir_path)
    except PermissionError:
        return "⛔️"
    
    if len(contents) == 0:
        return "📁"
    else:
        return "📂"

def format_tree_dir(dir_path: pathlib.Path, is_last_depth: bool) -> Text:
    """Return a formatted Text directory path to go to the Tree."""
    try:
        contents = os.listdir(dir_path)
    except PermissionError:
        contents = []
        style = "bold red"
        text_str = f"{folder_emoji(dir_path=dir_path)} {escape(dir_path.name)}"
    else:
        style = "dim cyan" if (dir_path.name.startswith(".") or 
                        dir_path.name.startswith("__") or
                        len(contents) == 0) else "cyan"
        text_str = f"{folder_emoji(dir_path=dir_path)} {escape(dir_path.name)}"

    # Add '...' if is_last_depth and the directory contains a file
    # end_index = len(text_str)
    if is_last_depth:
        if len(contents) > 0:
            text_str += " (...)"
            # end_index = len(text_str) - 6

    text = Text(
        text=text_str,
        style=style,
        # overflow="ellipsis",
    )
    # text.stylize(f"link file://{dir_path}", start=2, end=end_index)
    return text

def file_emoji(file_path: pathlib.Path) -> str:
    """Return the emoji for a file."""
    if file_path.suffix == ".py":
        return "🐍"
    elif file_path.suffix == ".md":
        return "📝"
    elif file_path.suffix == ".txt":
        return "📄"
    elif file_path.suffix == ".json":
        return "📝"
    elif file_path.suffix == ".yml":
        return "📝"
    elif file_path.suffix == ".toml":
        return "📝"
    elif file_path.suffix == ".c":
        return "📝"
    elif file_path.suffix == ".cpp":
        return "📝"
    elif file_path.suffix == ".v":
        return "📝"
    elif file_path.suffix == ".lmp":
        return "⚛️ "
    else:
        return "📄"

def format_tree_file(file_path: pathlib.Path) -> Text:
    """Return a formatted Text file path to go to the Tree."""
    try:
        file_size = decimal(file_path.stat().st_size)
        icon = file_emoji(file_path)
    except FileNotFoundError:
        file_size = "???"
        icon = "⛔️"

    style = "dim" if (file_path.name.startswith(".") or 
                      file_path.name.startswith("__")) else ""
    
    text_filename = Text(text=f"{icon} ", style=style)
    text_filename.append(f"{escape(file_path.name)}", style="green")
    # text_filename.stylize("dim", len(file_path.suffix))
    text_filename.highlight_regex(r"\.(py|js|html|css|md|txt|json|yml|yaml|toml|c|lmp|cpp|v)$", 
                                  "bold")
    # text_filename.stylize(f"link file://{file_path}", start=2)
    text_filename.append(f" ({file_size})", "blue")

    return text_filename

def walk_dir(directory: pathlib.Path, tree: Tree, 
             ignore_files: bool, ignore_dirs: bool, ignore_filetypes: bool,
             search_depth: int, maximum_depth: int = 3):
    """Walk a directory and add its contents to a tree."""
    
    # Sort dirs first then by filename
    try:
        paths = sorted(
            pathlib.Path(directory).iterdir(),
            key=lambda path: (path.is_file(), path.name.lower()),
        )
    except PermissionError as e:
        file_path = pathlib.Path(e.filename)
        tree.add(format_tree_file(file_path))
        return
    
    for path in paths:
        # Skip hidden files
        if path.name.startswith("."):
            continue

        # Skip ignored directories
        if path.is_dir() and ignore_dirs and path.name in IGNORED_DIRS:
            continue

        # Skip ignored files
        if path.is_file() and ignore_files and path.name in IGNORED_FILES:
            continue

        # Skip ignored filetypes
        if path.is_file() and ignore_filetypes and path.suffix in IGNORE_FILETYPES:
            continue

        # Do smth if path is a directory
        if path.is_dir():
            if search_depth < maximum_depth:
                child = tree.add(format_tree_dir(path, is_last_depth=False))
                walk_dir(path, child, ignore_files, ignore_dirs, ignore_filetypes,
                         search_depth + 1, maximum_depth)
            else:
                tree.add(format_tree_dir(path, is_last_depth=True))
        # Do smth if path is a file
        else:
            tree.add(format_tree_file(path))
