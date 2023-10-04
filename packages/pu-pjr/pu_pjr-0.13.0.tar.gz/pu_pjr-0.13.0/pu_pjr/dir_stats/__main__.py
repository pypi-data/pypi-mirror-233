import argparse
import pathlib
from rich.console import Console

# from . import utils
from . import dir_contents

def main():
    parser = argparse.ArgumentParser(
        description="Get information about directory contents.",
        prog="dirstats",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    parser.set_defaults(which="main")

    parser.add_argument(
        "--version", "-v", action="version", version="%(prog)s v0.13.0"
    )

    # Sub-parser for the "tree" command
    subparser = parser.add_subparsers()
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
        with console.status("[bold green]Getting directory contents..."):
            # Get absolute path
            path_dir = pathlib.Path(args.directory).resolve()

            if not path_dir.exists():
                console.log(f"Directory {path_dir} does not exist.")
                exit(1)

            tree = dir_contents.get_dir_contents(dir=path_dir, maximum_depth=args.depth)
            
            if args.pager:
                with console.pager():
                    console.print(tree)
            else:
                console.print(tree)
    elif args.which == "ext":
        with console.status("[bold green]Getting directory contents..."):
            # Get absolute path
            path_dir = pathlib.Path.cwd().resolve()

            if not path_dir.exists():
                console.log(f"Directory {path_dir} does not exist.")
                exit(1)

            dir_contents.find_files_type(path_dir, args.extensions, 0, 
                                                args.depth, args.abs, args.search_full)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()