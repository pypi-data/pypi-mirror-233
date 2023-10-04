from matplotlib import pyplot as plt
from . import utils

# Plotting x-y data from files
def plot_xy(
        filename: str, plot_all=False, xcol: int=0, ycol: int=1, sep: str=' ', 
        line_type: str = '-', 
        normalise: utils.Normalisation = utils.Normalisation.NONE, 
        mathematical_expression: None | str = None,
        mathematical_expression_location: utils.MathLocs = utils.MathLocs.BOTH,
        testing: bool = False, **kwargs
        ):
    df = utils.load_data(filename, sep=sep)

    # Normalise data
    if normalise == utils.Normalisation.STANDARD:
        df = utils.normalise(df)
    elif normalise == utils.Normalisation.ZERO_ONE:
        df = utils.normalise_0_1(df)
    else:
        if mathematical_expression is not None:
            df = utils.apply_math_expression(df, mathematical_expression,
                                        mathematical_expression_location,
                                        plot_all,
                                        xcol, ycol)

    if plot_all:
        for col in range(0, len(df.columns)):
            if col != xcol:
                plt.plot(df.iloc[:, xcol], df.iloc[:, col], line_type,
                         label=f"Col: {col}", **kwargs)
    else:
        x = df.iloc[:, xcol]
        y = df.iloc[:, ycol]
        plt.plot(x, y, line_type, label=f"Col: {ycol}", **kwargs)

    plt.legend()
    plt.title(f"{filename} xcol: {xcol} ycol: {ycol}")
    plt.grid()
    plt.show(block=not testing)
    
    return