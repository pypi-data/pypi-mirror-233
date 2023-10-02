import pandas as pd
from enum import Enum
import glob
import os

# Enum types of normalisation
class Normalisation(Enum):
    NONE = 0
    STANDARD = 1
    ZERO_ONE = 2

# Enum types of mathematical expressions applied to data
class MathLocs(Enum):
    X = 0
    Y = 1
    BOTH = 2

# Enum types of mathematical expressions
class MathTypes(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    POW = "^"

SPECIAL_VALS = ["MAX", "MIN", "MEAN", "STD"]

# Load to a pandas dataframe from a file
def load_data(filename: str, sep: str=' ', comment: str='#'):
    df = pd.read_csv(filename, sep=sep, comment=comment, header=None)
    return df

# Load many files into a pandas dataframe from a regex pattern
def load_many_data(pattern: str, dir: str = "./", sep: str=' ', comment: str='#'):
    #Change directory
    original_dir = os.getcwd()
    os.chdir(dir)

    filenames = glob.glob(pattern)
    # Sort the filenames
    filenames.sort()

    dfs = []
    for filename in filenames:
        df = load_data(filename, sep=sep, comment=comment)
        dfs.append(df)

    #Change back to original directory
    os.chdir(original_dir)
  
    return dfs, filenames

# Normalise data
def normalise(df: pd.DataFrame) -> pd.DataFrame:
    df = (df - df.mean()) / df.std()
    return df

# Change range of data to [0, 1]
def normalise_0_1(df: pd.DataFrame) -> pd.DataFrame:
    df = (df - df.min()) / (df.max() - df.min())
    return df

# Parse a mathematical expression
def parse_math_expression(expression: str) -> dict[str, int]:
    # Split the expression into x and y parts
    parts = expression.split(',')

    d = []
    for part in parts:
        # Split the part into variable and expression
        type, val = part.split('|')
        if type.strip() not in [t.value for t in MathTypes]:
            raise ValueError(f"Invalid mathematical type: {type}")
        try:
            value = float(val.strip())
        except ValueError:
            if val in SPECIAL_VALS:
                value = val
            else:
                raise ValueError(f"Invalid mathematical value: {val}")

        d.append((type.strip(), value))

    return d

def calculate_special_val(df: pd.DataFrame, speciel_val: str) -> list[float]:
    if speciel_val == "MIN":
        return df.min()
    elif speciel_val == "MAX":
        return df.max()
    elif speciel_val == "MEAN":
        return df.mean()
    elif speciel_val == "STD":
        return df.std()
    else:
        return [0.0]*df.shape[1]

# Apply a mathematical expression to a dataframe column
def apply_math_expression(df: pd.DataFrame, expression: str, 
                          location: MathLocs = MathLocs.BOTH,
                          plot_all: bool = False,
                          xcol: int = 0, ycol: int = 1) -> pd.DataFrame:
    # Parse the expression
    d = parse_math_expression(expression)

    # Apply the expression
    if location is MathLocs.X or location is MathLocs.BOTH:
        for type, val in d:
            if val in SPECIAL_VALS:
                val = calculate_special_val(df, val)
            else:
                val = [val]*df.shape[1]

            if type == MathTypes.ADD.value:
                df.iloc[:, xcol] = df.iloc[:, xcol] + val[xcol]
            elif type == MathTypes.SUB.value:
                df.iloc[:, xcol] = df.iloc[:, xcol] - val[xcol]
            elif type == MathTypes.MUL.value:
                df.iloc[:, xcol] = df.iloc[:, xcol] * val[xcol]
            elif type == MathTypes.DIV.value:
                df.iloc[:, xcol] = df.iloc[:, xcol] / val[xcol]
            elif type == MathTypes.POW.value:
                df.iloc[:, xcol] = df.iloc[:, xcol] ** val[xcol]
            else:
                raise ValueError(f"Invalid mathematical type: {type}")

    if location is MathLocs.Y or location is MathLocs.BOTH:
        for type, val in d:
            if val in SPECIAL_VALS:
                val = calculate_special_val(df, val)
            else:
                val = [val]*df.shape[1]

            if type == MathTypes.ADD.value:
                if plot_all:
                    for col in range(0, len(df.columns)):
                        if col != xcol:
                            df.iloc[:, col] = df.iloc[:, col] + val[col]
                else:
                    df.iloc[:, ycol] = df.iloc[:, ycol] + val[ycol]
            elif type == MathTypes.SUB.value:
                if plot_all:
                    for col in range(0, len(df.columns)):
                        if col != xcol:
                            df.iloc[:, col] = df.iloc[:, col] + val[col]
                else:
                    df.iloc[:, ycol] = df.iloc[:, ycol] - val[ycol]
            elif type == MathTypes.MUL.value:
                if plot_all:
                    for col in range(0, len(df.columns)):
                        if col != xcol:
                            df.iloc[:, col] = df.iloc[:, col] + val[col]
                else:
                    df.iloc[:, ycol] = df.iloc[:, ycol] * val[ycol]
            elif type == MathTypes.DIV.value:
                if plot_all:
                    for col in range(0, len(df.columns)):
                        if col != xcol:
                            df.iloc[:, col] = df.iloc[:, col] + val[col]
                else:
                    df.iloc[:, ycol] = df.iloc[:, ycol] / val[ycol]
            elif type == MathTypes.POW.value:
                if plot_all:
                    for col in range(0, len(df.columns)):
                        if col != xcol:
                            df.iloc[:, col] = df.iloc[:, col] + val[col]
                else:
                    df.iloc[:, ycol] = df.iloc[:, ycol] ** val[ycol]
            else:
                raise ValueError(f"Invalid mathematical type: {type}")

    return df