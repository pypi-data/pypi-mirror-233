from matplotlib import pyplot as plt
from . import utils

# Plot data from multiple files
def plot_multifile_xy(
        pattern: str, dir: str = "./", xcol: int = 0, ycol: int=1, sep: str=' ',
        line_style: str = "-",
        equal_axes: bool = False,
        single_plot: bool = False,
        testing: bool = False, **kwargs
        ):
    dfs, filenames = utils.load_many_data(pattern, sep=sep, dir=dir) # Load data

    # Find the x and y ranges so that all data can be plotted on the same axes
    if equal_axes:
        x_min = min([df.iloc[:, xcol].min() for df in dfs])
        x_max = max([df.iloc[:, xcol].max() for df in dfs])
        y_min = min([df.iloc[:, ycol].min() for df in dfs])
        y_max = max([df.iloc[:, ycol].max() for df in dfs])

    # Plot each file in subplots
    # Get number of files
    n_files = len(dfs)

    # Create figure and axes
    if single_plot:
        fig, axes = plt.subplots(ncols=1, nrows=1)#, figsize=(12, 6))
    else:
        fig, axes = plt.subplots(ncols=1, nrows=n_files)#, figsize=(12, 6))
    # _, axes = plt.subplots(ncols=1, nrows=n_files)#, figsize=(12, 6))

    # Plot each file
    for i in range(n_files):
        df = dfs[i]
        x = df.iloc[:, xcol]
        y = df.iloc[:, ycol]
        if single_plot:
            axes.plot(x, y, line_style, label=f"File: {filenames[i]}", **kwargs)
            axes.legend()
        else:
            axes[i].plot(x, y, line_style, **kwargs)
            axes[i].set_xlabel(f"File: {filenames[i]}")
            # axes[i].set_ylabel("y")
            axes[i].grid()
            if equal_axes:
                axes[i].set_xlim(x_min, x_max)
                axes[i].set_ylim(y_min, y_max)

    plt.suptitle(pattern)
    plt.show(block=not testing)

def plot_multifile_bar(
        pattern: str, dir: str = "./", col: int=1, sep: str=' ',
        special_val: str = "MAX",
        testing: bool = False, **kwargs
        ):
    dfs, filenames = utils.load_many_data(pattern, sep=sep, dir=dir) # Load data

    # Plot in bar chart
    # Calculate the special value for each file
    special_vals = []
    for df in dfs:
        special_vals_cols = utils.calculate_special_val(df, special_val)
        special_vals.append(special_vals_cols[col])

    # Plot the special values
    plt.bar(filenames, special_vals, **kwargs)
    plt.xlabel("Filenames")

    plt.suptitle(pattern + " " + special_val + " of column " + str(col))
    plt.show(block=not testing)

    return
