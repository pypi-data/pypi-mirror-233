import argparse
from rich.console import Console
from rich.text import Text

from . import utils
from . import force_fields

def main():
    parser = argparse.ArgumentParser(
        description="Plot potentials.",
        prog="potentials",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    parser.set_defaults(which="main")

    parser.add_argument(
        "--version", "-v", action="version", version="%(prog)s v0.20.0"
    )

    subparsers = parser.add_subparsers(title="subcommands", dest="which")
    list_parser = subparsers.add_parser(
        "list", help="list available force fields",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    list_parser.set_defaults(which="list")

    plot_parser = subparsers.add_parser(
        "show", help="plot a force field",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    plot_parser.set_defaults(which="main")

    plot_parser.add_argument(
        "--together", "-t", action="store_true",
        help = "Plot all potentials together, if not the potentials will" +
               " be plotted one by one default False"
    )
    plot_parser.add_argument(
        "--y-range", "-y", type=float, nargs=2, default=[-5.0, 10.0],
        help = "Min value for range in plot points, default 0.9"
    )
    plot_parser.add_argument(
        "--range-min", "-r", type=float, default=0.9,
        #metavar="kwargs",
        help = "Min value for range in plot points, default 0.9"
    )
    plot_parser.add_argument(
        "--range-max", "-R", type=float, default=3.0,
        #metavar="kwargs",
        help = "Min value for range in plot points, default 3.0"
    )
    plot_parser.add_argument(
        "--range-points", "-p", type=int, default=30,
        #metavar="kwargs",
        help = "Number of points in range, default 30"
    )
    plot_parser.add_argument(
        "--line-type", "-l", type=str, default="o-",
        #metavar="kwargs",
        help = "Line type for plot, default 'o-'"
    )
    plot_parser.add_argument(
        "--from-file", "-f", action="store_true", dest="read_from_file",
        #metavar="kwargs",
        help = "Read arguments from file, ignores other potential_data arguments"
    )
    plot_parser.add_argument(
        "--file-name", "-F", type=str, default="potentials.pot",
        #metavar="kwargs",
        help = "File name to read arguments from, default 'potentials.pot'"
    )
    plot_parser.add_argument(
        "potential_data", nargs="*",
        #metavar="kwargs",
        help = "Force field data to plot POTENTIAL must be a valid field name and DATA"+
            " must be valid keyword arguments for the potential."
    )

    args = parser.parse_args()
    # print(args)

    console = Console()
    if args.which == "main":
        if args.read_from_file:
            try:
                with open(args.file_name, "r") as f:
                    # Remove newlines and split by spaces, eliminate multiple spaces
                    args.potential_data = " ".join(f.read().replace("\n", " ").split())\
                        .split(" ")
            except FileNotFoundError as e:
                console.print(f"⛔️[bold red]FILE NOT FOUND ERROR: "
                              f"[bold yellow][underline]{e.filename}[/underline]"
                              f" is not a valid file")
                exit(4)
            except PermissionError as e:
                console.print(f"⛔️[bold red]PERMISSION ERROR: "
                              f"[bold yellow][underline]{e.filename}[/underline]"
                              f" cannot be read")
                exit(5)
            
            # print(args.potential_data)
        
        try:
            keyargpairs = utils.parse_keyargpairs(args.potential_data)
            # print(keyargpairs)
        except ValueError as e:
            console.print(f"⛔️[bold red]VALUE ERROR: [bold yellow]{e}")
            exit(1)
        except TypeError as e:
            console.print(f"⛔️[bold red]TYPE ERROR: [bold yellow]{e}")
            exit(3)
        except KeyError as e:
            console.print(f"⛔️[bold red]KEY ERROR: "
                          f"[bold yellow][underline]{e}[/underline]"
                          f" is not a valid potential name")
            exit(2)

        try:
            points = utils.create_range(args.range_min, 
                                        args.range_max, 
                                        args.range_points)
        except ValueError as e:
            console.print(f"⛔️[bold red]VALUE ERROR: [bold yellow]{e}")
            exit(1)
        
        try:
            potentials = [utils.Potentials[utils.remove_extras_for_class(field)] \
                            for field in keyargpairs]
            potential_args = [keyargpairs[field] for field in keyargpairs]
        except KeyError as e:
            console.print(f"⛔️[bold red]KEY ERROR: "
                          f"[bold yellow][underline]{e}[/underline]"
                          f" is not a valid potential name")
            exit(2)

        with console.status("[bold green]Plot created"):
            if args.together:
                # potentials = [utils.Potentials[utils.remove_extras_for_class(field)] \
                #               for field in keyargpairs]
                # potential_args = [keyargpairs[field] for field in keyargpairs]
                try:
                    force_fields.plot_fields_single(potentials, 
                                                    potential_args, 
                                                    points, 
                                                    args.line_type,
                                                    args.y_range)
                except ValueError as e:
                        console.print(f"⛔️[bold red]VALUE ERROR: [bold yellow]{e}")
                        exit(1)
                except TypeError as e:
                    console.print(f"⛔️[bold red]TYPE ERROR: [bold yellow]{e}")
                    exit(3)
            else:
                for pos in range(len(potentials)):
                    try:
                        force_fields.plot_field(potentials[pos], 
                                                points, 
                                                args.line_type,
                                                args.y_range,
                                                **potential_args[pos])
                    except ValueError as e:
                        console.print(f"⛔️[bold red]VALUE ERROR: [bold yellow]{e}")
                        exit(1)
                    except TypeError as e:
                        console.print(f"⛔️[bold red]TYPE ERROR: [bold yellow]{e}")
                        exit(3)

    elif args.which == "list":
        descriptions, max_length = utils.field_descriptions()
        for field in descriptions:
            text = Text(f"{field.replace('/', '_'):>{max_length}}: "
                        f"{descriptions[field]}")
            text.stylize("bold green", 0, max_length)
            text.stylize("bold blue", max_length + 2, len(text))
            text.highlight_regex("ARGS:.*", "bold yellow")
            console.print(text)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()