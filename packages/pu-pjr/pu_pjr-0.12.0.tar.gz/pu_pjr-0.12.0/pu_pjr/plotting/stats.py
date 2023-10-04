from matplotlib import pyplot as plt
from . import utils

# Show violin plot of data from file
def violin_plot(
        filename: str, col: int=-1, sep: str=' ', 
        testing: bool = False, **kwargs
        ):
    df = utils.load_data(filename, sep=sep) # Load data

    if col != -1:
        data = df.iloc[:, col]

        plt.violinplot(data, showmedians=True, **kwargs)
        plt.xlabel(f"Column: {col}")
        # plt.ylabel("y")
        plt.title(filename)
        plt.grid(axis='y') # Grid lines only on y-axis
        plt.show(block=not testing)
    else:
        # Plot all columns in subplots
        # Get number of columns
        n_cols = df.shape[1]

        # Create figure and axes
        _, axes = plt.subplots(nrows=1, ncols=n_cols)#, figsize=(12, 6))

        # Plot each column
        for i in range(n_cols):
            data = df.iloc[:, i]
            axes[i].violinplot(data, showmedians=True, **kwargs)
            axes[i].set_xlabel(f"Column: {i}")
            # axes[i].set_ylabel("y")
            axes[i].grid(axis='y')

        plt.suptitle(filename)
        plt.show(block=not testing)

    return