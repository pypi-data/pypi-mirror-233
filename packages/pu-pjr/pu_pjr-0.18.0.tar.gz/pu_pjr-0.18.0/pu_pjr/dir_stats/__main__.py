import argparse
import pathlib
from rich.console import Console

# from . import utils
from . import dir_contents
from . import utils

def main():
    parser = argparse.ArgumentParser(
        description="Get information about directory contents.",
        prog="dirstats",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    parser.set_defaults(which="main")

    parser.add_argument(
        "--version", "-v", action="version", version="%(prog)s v0.18.0"
    )

    subparser = parser.add_subparsers(required=True)

    # Edit the listed file, directory, or filetype to ignore
    file_parser = subparser.add_parser(
        "ignore-files", help="Edit the files, directories, or filetypes to ignore",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    file_parser.set_defaults(which="ignore")

    file_parser.add_argument(
        "--file", "-f", type=str, choices=["dirs", "files", "filetypes"],
        required=True, help="The file to edit"
    )
    file_subparser = file_parser.add_subparsers(required=True)
    file_show_parser = file_subparser.add_parser(
        "show", help="Show the contents",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    file_show_parser.set_defaults(which="ignore-show")

    file_edit_parser = file_subparser.add_parser(
        "edit", help="Edit the contents",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    file_edit_parser.set_defaults(which="ignore-edit")

    file_edit_parser.add_argument(
        "--add", "-a", type=str, nargs="+",
        help="Add the file, directory, or filetype to ignore"
    )
    file_edit_parser.add_argument(
        "--remove", "-r", type=str, nargs="+",
        help="Remove the file, directory, or filetype to ignore"
    )

    # Sub-parser for the "tree" command
    tree_parser = subparser.add_parser(
        "tree", help="Get a tree of the directory contents",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    tree_parser.set_defaults(which="tree")

    tree_parser.add_argument(
        "--directory", "-D", type=str, default="./",
        help="The directory to get the contents of"
    )
    tree_parser.add_argument(
        "--depth", "-d", type=int, default=2,
        help="The maximum depth to search for files and folders. Default is 2"
    )
    tree_parser.add_argument(
        "--pager", "-p", action="store_true",
        help="Show the output in a pager"
    )
    tree_parser.add_argument(
        "--ignore-hidden-dirs", "-i", action="store_true",
        help="Ignore hidden directories (directories that start with a dot)"
    )
    tree_parser.add_argument(
        "--ignore-dirs-listed", action="store_true",
        help="Ignore dirs in list"
    )
    tree_parser.add_argument(
        "--ignore-files-listed", action="store_true",
        help="Ignore files in list"
    )
    tree_parser.add_argument(
        "--ignore-filetypes-listed", action="store_true",
        help="Ignore filetypes in list"
    )

    ext_parser = subparser.add_parser(
        "ext", help="Find files by extensions",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    ext_parser.set_defaults(which="ext")

    # tree_parser.add_argument(
    #     "--directory", "-D", type=str, default="./",
    #     help="The directory to get the contents of"
    # )
    ext_parser.add_argument(
        "--extensions", "-e", type=str, nargs="+", default=[".py"],
        help="The extensions to search for"
    )
    ext_parser.add_argument(
        "--depth", "-d", type=int, default=2,
        help="The maximum depth to search for files and folders. Default is 2"
    )
    ext_parser.add_argument(
        "--abs", "-a", action="store_true",
        help="Set to show absolute paths instead of relative paths"
    )
    ext_parser.add_argument(
        "--search-full", "-s", action="store_true",
        help="Search the full tree instead of the depth specified"
    )
    ext_parser.add_argument(
        "--ignore-hidden-dirs", "-i", action="store_true",
        help="Ignore hidden directories (directories that start with a dot)"
    )

    reg_parser = subparser.add_parser(
        "reg", help="Find files by regex expression",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    reg_parser.set_defaults(which="reg")

    # tree_parser.add_argument(
    #     "--directory", "-D", type=str, default="./",
    #     help="The directory to get the contents of"
    # )
    reg_parser.add_argument(
        "--expression", "-e", type=str, default="", required=True,
        help="The regex expression to search for"
    )
    reg_parser.add_argument(
        "--depth", "-d", type=int, default=2,
        help="The maximum depth to search for files and folders. Default is 2"
    )
    reg_parser.add_argument(
        "--abs", "-a", action="store_true",
        help="Set to show absolute paths instead of relative paths"
    )
    reg_parser.add_argument(
        "--search-full", "-s", action="store_true",
        help="Search the full tree instead of the depth specified"
    )
    reg_parser.add_argument(
        "--ignore-hidden-dirs", "-i", action="store_true",
        help="Ignore hidden directories (directories that start with a dot)"
    )

    # console = Console()

    # console.print("Hello", "World", ":smile:", 
    #               style="bold red")
    
    # table = Table(title="Table title")

    # table.add_column(header="Test")
    # table.add_column(header="Content", )

    # table.add_row("Item 1")

    # console.print(table)

    # table = dir_contents.get_dir_contents()
    # console = Console()
    
    # with console.pager():
    #     console.print(table)

    args = parser.parse_args()

    console = Console()
    if args.which == "tree":
        # Get absolute path
        path_dir = pathlib.Path(args.directory).resolve()

        if not path_dir.exists():
            console.log(f"Directory {path_dir} does not exist.")
            exit(1)

        tree = dir_contents.get_dir_contents(dir=path_dir, maximum_depth=args.depth,
                                                ignore_hidden_dirs=args.ignore_hidden_dirs,
                                                ignore_dirs=args.ignore_dirs_listed,
                                                ignore_files=args.ignore_files_listed,
                                                ignore_filetypes=args.ignore_filetypes_listed)
        
        if args.pager:
            with console.pager():
                console.print(tree)
        else:
            console.print(tree)
    elif args.which == "ext":
        # Get absolute path
        path_dir = pathlib.Path.cwd().resolve()

        if not path_dir.exists():
            console.log(f"Directory {path_dir} does not exist.")
            exit(1)

        dir_contents.find_files_type(path_dir, args.extensions, 0, 
                                    args.depth, args.abs, args.search_full,
                                    args.ignore_hidden_dirs)
    elif args.which == "reg":
        # Get absolute path
        path_dir = pathlib.Path.cwd().resolve()

        if not path_dir.exists():
            console.log(f"Directory {path_dir} does not exist.")
            exit(1)

        dir_contents.find_files_expression(path_dir, args.expression, 0, 
                                            args.depth, args.abs, args.search_full,
                                            args.ignore_hidden_dirs)
    elif args.which == "ignore-show":
        if args.file == "dirs":
            dirs = utils.ignored_dirs_list()
            if len(dirs) == 0:
                console.print("No directories ignored.")
            else:
                console.print(dirs)
        elif args.file == "files":
            files = utils.ignored_files_list()
            if len(files) == 0:
                console.print("No files ignored.")
            else:
                console.print(files)
        elif args.file == "filetypes":
            filetypes = utils.ignored_filetypes_list()
            if len(filetypes) == 0:
                console.print("No filetypes ignored.")
            else:
                console.print(filetypes)
    elif args.which == "ignore-edit":
        if args.add is not None:
            utils.add_to_file(args.file, args.add)
        if args.remove is not None:
            utils.remove_from_file(args.file, args.remove)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()