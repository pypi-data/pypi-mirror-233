import argparse

from . import utils
from . import xy
from . import stats
from . import multi_file

def main():
    parser = argparse.ArgumentParser(
        description="Plot data from a file.",
        prog="quickplot",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    parser.set_defaults(which="main")

    parser.add_argument(
        "--version", "-v", action="version", version="%(prog)s v0.12.0"
    )

    # Sub-parser for the "xy" command
    subparser = parser.add_subparsers()
    plot_xy_parser = subparser.add_parser(
        "xy", help="Plot x-y data",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    plot_xy_parser.set_defaults(which="xy")

    plot_xy_parser.add_argument(
        "filename", type=str, help="The data file to plot"
    )
    plot_xy_parser.add_argument(
        "--all", "-a", action="store_true",
        help="Plot all columns against the defined x column"
    )
    normalisation_types = [n.name for n in utils.Normalisation]
    plot_xy_parser.add_argument(
        "--normalise", "-n", type=str, 
        choices=normalisation_types, 
        default=utils.Normalisation.NONE.name,
        help="""
        Normalise the data. Choices are:
        (Default) NONE: No normalisation. 
        STANDARD: Standard normalisation
        ZERO_ONE: Normalise to the range [0, 1]
        """
    )
    plot_xy_parser.add_argument(
        "--xcol", "-x", type=int, default=0, 
        help="The column containing x values, index starts at 0. Default is 0"
    )
    plot_xy_parser.add_argument(
        "--ycol", "-y", type=int, default=1, 
        help="The column containing y values, index starts at 0. Default is 1"
    )
    plot_xy_parser.add_argument(
        "--separator", "-s", type=str, default=" ", 
        help="The separator between columns, default is (space)"
    )
    plot_xy_parser.add_argument(
        "--line", "-l", type=str, default='-', 
        help="Line type, default is solid line (-)"
    )
    math_locs = [n.name for n in utils.MathLocs]
    plot_xy_parser.add_argument(
        "--math-loc", "-m", type=str, 
        choices=math_locs, 
        default=utils.MathLocs.X.name,
        help="""
        Where to apply the mathematical transformation. Choices are:
        (Default) X: x-axis only.
        Y: y-axis only
        BOTH: x and y axes
        """
    )
    plot_xy_parser.add_argument(
        "--math-exp", "-M", type=str, default='#', 
        help="""
        The mathematical expression. In the format: {+,-,*,/,^}|{num},...
        {num} can use the special values: MAX, MIN, MEAN, STD
        """
    )

    # Sub-parser for the "stats" command
    plot_stats_parser = subparser.add_parser(
        "stats", help="Violin plot of the data",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    plot_stats_parser.set_defaults(which="stats")

    plot_stats_parser.add_argument(
        "filename", type=str, help="The data file to plot"
    )
    plot_stats_parser.add_argument(
        "--col", "-c", type=int, default=-1, 
        help="The column to plot starting from 0, default is all columns (-1)"
    )

    # Sub-parser for the "multi" command
    plot_stats_parser = subparser.add_parser(
        "multi", help="PLot from multiple files",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    plot_stats_parser.set_defaults(which="multi")

    plot_stats_parser.add_argument(
        "pattern", type=str, help="The pattern to match the file names eg. *.txt"
    )
    plot_stats_parser.add_argument(
        "--dir", "-d", type=str, default="./", 
        help="The directory to search for files, default is current directory"
    )
    multiplot_types = plot_stats_parser.add_subparsers(
        title="Plot type", dest="plot_type", required=True
    )
    multiplot_xy_parser = multiplot_types.add_parser(
        "xy", help="Plot x-y data",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    multiplot_xy_parser.set_defaults(which="multi-xy")

    multiplot_xy_parser.add_argument(
        "--xcol", "-x", type=int, default=0, 
        help="The column containing x values, index starts at 0. Default is 0"
    )
    multiplot_xy_parser.add_argument(
        "--ycol", "-y", type=int, default=1, 
        help="The column containing y values, index starts at 0. Default is 1"
    )
    multiplot_xy_parser.add_argument(
        "--separator", "-s", type=str, default=" ", 
        help="The separator between columns, default is (space)"
    )
    multiplot_xy_parser.add_argument(
        "--line-type", "-l", type=str, default='-', 
        help="Line type, default is solid line (-)"
    )
    multiplot_xy_parser.add_argument(
        "--equal-axes", "-e", action="store_true",
        help="Make all axes the same"
    )
    multiplot_xy_parser.add_argument(
        "--single-plot", "-S", action="store_true",
        help="Plot all files on the same plot"
    )

    multiplot_bar_parser = multiplot_types.add_parser(
        "bar", help="Bar plot of the data",
        epilog="Created by Pedro Juan Royo @UnstrayCato"
    )
    multiplot_bar_parser.set_defaults(which="multi-bar")

    multiplot_bar_parser.add_argument(
        "--col", "-c", type=int, default=1, 
        help="The column to plot starting from 0, default is 1"
    )
    multiplot_bar_parser.add_argument(
        "--special-val", "-s", type=str, default="MAX",
    )

    args = parser.parse_args()

    if args.which == "xy":
        math_exp = None if args.math_exp == "#" else args.math_exp
        try:
            xy.plot_xy(args.filename, plot_all=args.all, xcol=args.xcol, 
                       ycol=args.ycol, sep=args.separator, line_type=args.line, 
                       normalise=utils.Normalisation[args.normalise],
                       mathematical_expression_location=utils.MathLocs[args.math_loc],
                       mathematical_expression=math_exp)
        except FileNotFoundError as e:
            print(f"FILE NOT FOUND. Filename: {e.filename}")
            exit(1)
        except IndexError as e:
            print(f"INDEX ERROR. Column: {e.args[0]}")
            exit(2)
        except ValueError as e:
            print(f"VALUE ERROR. {e.args[0]}")
            exit(3)
    elif args.which == "stats":
        try:
            stats.violin_plot(args.filename, args.col)
        except FileNotFoundError as e:
            print(f"FILE NOT FOUND. Filename: {e.filename}")
            exit(1)
        except IndexError as e:
            print(f"INDEX ERROR. Column: {e.args[0]}")
            exit(2)
        except ValueError as e:
            print(f"VALUE ERROR. {e.args[0]}")
            exit(3)
    elif args.which == "multi-bar":
        try:
            multi_file.plot_multifile_bar(args.pattern, dir=args.dir, col=args.col, 
                                          special_val=args.special_val)
        except FileNotFoundError as e:
            print(f"FILE NOT FOUND. Filename: {e.filename}")
            exit(1)
        except IndexError as e:
            print(f"INDEX ERROR. Column: {e.args[0]}")
            exit(2)
        except ValueError as e:
            print(f"VALUE ERROR. {e.args[0]}")
            exit(3)
    elif args.which == "multi-xy":
        try:
            multi_file.plot_multifile_xy(args.pattern, dir=args.dir, xcol=args.xcol, 
                                         ycol=args.ycol, sep=args.separator,
                                         equal_axes=args.equal_axes,
                                         single_plot=args.single_plot,
                                         line_style=args.line_type)
        except FileNotFoundError as e:
            print(f"FILE NOT FOUND. Filename: {e.filename}")
            exit(1)
        except IndexError as e:
            print(f"INDEX ERROR. Column: {e.args[0]}")
            exit(2)
        except ValueError as e:
            print(f"VALUE ERROR. {e.args[0]}")
            exit(3)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()