import os
import pathlib

from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.tree import Tree
from rich import print

ALLOWED_FILENAMES = ["dirs", "files", "filetypes"]

IGNORED_DIRS = [".git", ".venv", "__pycache__", "node_modules"]
IGNORED_FILES = [".DS_Store", ".gitignore", ".python-version", 
                 "__init__.py", "__main__.py"]
IGNORE_FILETYPES = [".ignore", ".pyc"]

IMG_FILETYPES = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".bmp")

FILE_PATH = pathlib.Path("/Users/parzival1918/.dirstats")

def read_from_file(file_name: str) -> list[str]:
    """Read a list of strings from a file."""
    # Check if file_name is allowed
    if file_name not in ALLOWED_FILENAMES:
        raise ValueError(f"File name {file_name} is not allowed.")
    
    # Check if file exists
    if not (FILE_PATH / file_name).exists():
        # Create directory if it doesn't exist
        if not FILE_PATH.exists():
            print("Creating directory /Users/parzival1918/.dirstats")
            FILE_PATH.mkdir()

        # Create file
        with open(FILE_PATH / file_name, "w") as f:
            # Write the default values
            if file_name == "dirs":
                f.write("\n".join(IGNORED_DIRS))
            elif file_name == "files":
                f.write("\n".join(IGNORED_FILES))
            elif file_name == "filetypes":
                f.write("\n".join(IGNORE_FILETYPES))

    with open(FILE_PATH / file_name, "r") as f:
        return [line.strip() for line in f.readlines()]
    
def ignored_dirs_list() -> list[str]:
    """Return a list of ignored directories."""
    return read_from_file("dirs")

def ignored_files_list() -> list[str]:
    """Return a list of ignored files."""
    return read_from_file("files")

def ignored_filetypes_list() -> list[str]:
    """Return a list of ignored filetypes."""
    return read_from_file("filetypes")

def add_to_file(file_name: str, items: list[str]) -> None:
    """Add items to a file."""
    items_already_in_file = read_from_file(file_name)
    items_to_add = []
    for item in items:
        if item not in items_already_in_file:
            items_to_add.append(item)
        else:
            text = Text(f"{item} already in {file_name}.", style="bold yellow")
            print(text)

    if len(items_to_add) > 0:
        with open(FILE_PATH / file_name, "a") as f:
            f.write("\n")
            f.write("\n".join(items_to_add))
    
    text = Text(f"Added {len(items_to_add)} items to {file_name}.", style="green")
    if len(items_to_add) > 0:
        text.append(f" {items_to_add}", style="bold green")
    print(text)

def remove_from_file(file_name: str, items: list[str]) -> None:
    """Remove items from a file."""
    items_already_in_file = read_from_file(file_name)
    items_to_remove = []
    for item in items:
        if item in items_already_in_file:
            items_to_remove.append(item)
        else:
            text = Text(f"{item} not in {file_name}.", style="bold yellow")
            print(text)

    if len(items_to_remove) > 0:
        with open(FILE_PATH / file_name, "w") as f:
            f.write("\n".join([item for item in items_already_in_file 
                               if item not in items_to_remove]))
    
    text = Text(f"Removed {len(items_to_remove)} items from {file_name}.", 
                style="green")
    if len(items_to_remove) > 0:
        text.append(f" {items_to_remove}", style="bold green")
    print(text)

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
    elif file_path.suffix == ".data":
        return "📊"
    elif file_path.suffix == ".xy":
        return "📈"
    elif file_path.suffix in IMG_FILETYPES:
        return "🖼"
    elif file_path.suffix == ".pdf":
        return "📑"
    elif file_path.suffix == ".html":
        return "🕸️"
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
             ignore_hidden_dirs: bool,
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
        if path.name.startswith(".") and ignore_hidden_dirs:
            continue

        # Skip ignored directories
        if path.is_dir() and ignore_dirs and path.name in ignored_dirs_list():
            continue

        # Skip ignored files
        if path.is_file() and ignore_files and path.name in ignored_files_list():
            continue

        # Skip ignored filetypes
        if path.is_file() and ignore_filetypes and \
            path.suffix in ignored_filetypes_list():
            continue

        # Do smth if path is a directory
        if path.is_dir():
            if search_depth < maximum_depth:
                child = tree.add(format_tree_dir(path, is_last_depth=False))
                walk_dir(path, child, ignore_files, ignore_dirs, ignore_filetypes,
                         ignore_hidden_dirs,
                         search_depth + 1, maximum_depth)
            else:
                tree.add(format_tree_dir(path, is_last_depth=True))
        # Do smth if path is a file
        else:
            tree.add(format_tree_file(path))
