from matplotlib import pyplot as plt

from . import utils

def get_field_data(
    field: utils.Potentials, points: list[float], **kwargs
) -> list[float]:
    """Get the values for some points in a potential"""
    if field == utils.Potentials.lj_cut:
        # print("lj/cut potential")
        return utils.lj_cut(points, **kwargs)
    elif field == utils.Potentials.buck:
        # print("buck potential")
        return utils.buck(points, **kwargs)
    elif field == utils.Potentials.buck_coul:
        # print("buck_coul potential")
        return utils.buck_coul(points, **kwargs)
    else:
        raise NotImplementedError(f'Field {field} not implemented')
    
def plot_field(
    field: utils.Potentials = utils.Potentials.lj_cut, 
    points: list[float] = utils.create_range(), 
    line_type: str = 'o-',
    y_range: list[float] = [-5.0, 10.0],
    **kwargs
) -> None:
    """Plot a potential"""

    x = points
    y = get_field_data(field, points, **kwargs)
    # print(x, len(x))
    # print(y)

    # line at y = 0
    plt.axhline(y=0, color='k')

    # if 'cut' in kwargs add vertical line at cut with label
    if 'cut' in kwargs:
        plt.axvline(x=kwargs['cut'], color='k', linestyle='--', label='cut')
        plt.legend(draggable=True)

    # Set y range 
    plt.ylim(y_range)

    plt.title(f"{utils.remove_extras_from_field_name(field.name)}: {kwargs}")
    plt.plot(x, y, line_type)

    plt.xlabel("r")
    plt.ylabel("V(r)")

    plt.show(block=True)

def plot_fields_single(
    fields: list[utils.Potentials],
    args: list[dict[str, float]],
    points: list[float] = utils.create_range(),
    line_type: str = 'o-',
    y_range: list[float] = [-5.0, 10.0],
) -> None:
    """Plot a list of potentials on the same plot"""

    # Check that the number of fields and args match
    if len(fields) != len(args):
        raise ValueError(f"Number of fields ({len(fields)}) "
                         f"and args ({len(args)}) must match")

    for pos in range(len(fields)):
        # plot_field(fields[pos], points, line_type, y_range, **args[pos])
        x = points
        y = get_field_data(fields[pos], points, **args[pos])

        # line at y = 0
        plt.axhline(y=0, color='k')

        line = plt.plot(x, y, line_type, 
                 label=f"{utils.remove_extras_from_field_name(fields[pos].name)}:"
                 f" {args[pos]}")
        
        # Assign the same colour to the vertical line as the plot line
        if 'cut' in args[pos]:
            plt.axvline(x=args[pos]['cut'], color=line[0].get_color(), linestyle='--')


    plt.legend(draggable=True)
    plt.ylim(y_range)

    plt.xlabel("r")
    plt.ylabel("V(r)")

    plt.show(block=True)