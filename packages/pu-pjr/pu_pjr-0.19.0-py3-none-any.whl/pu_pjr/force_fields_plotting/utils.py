from enum import Enum
import math

### Constants ###

class Potentials(Enum):
    lj_cut = 'Lennard-Jones potential with a cut-off. ARGS: epsilon, sigma, cut'
    buck = 'Buckingham potential. ARGS: A, rho, C'
    buck_coul = 'Buckingham potential with Coulombic term. ARGS: A, rho, C, q1, q2'

def field_descriptions() -> (dict, int):
    """Return a description for all potentials"""
    descpritions = {}
    max_length = 0
    for field in Potentials:
        if len(field.name) > max_length:
            max_length = len(field.name)

        descpritions[field.name] = field.value

    return descpritions, max_length

def create_range(
    start: float = 0.1, end: float = 3.0, items: int = 30
) -> list[float]:
    """Return a float range between 'start' and 'end'"""
    # Check end is bigger than start
    if start >= end:
        raise ValueError("start value is bigger than end value")
    
    # Check that items is bigger than 1
    if items <= 1:
        raise ValueError("items value must be bigger than 1")

    step_val = (end - start) / (items - 1)
    range_vals = []
    for i in range(items):
        range_vals.append(start + step_val*i)

    return range_vals

def remove_extras_from_field_name(
    field_name: str
) -> str:
    """Remove extra characters from a potential name"""
    return field_name.split("-")[0].replace("_", "/")

def remove_extras_for_class(
    field_name: str
) -> str:
    """Remove extra characters from a potential name"""
    return field_name.split("-")[0]

def parse_keyargpairs(
    keyargpairs: list[str]
) -> dict[str, str]:
    """Parse a list of key-argument pairs"""
    keyargdict = {}
    current_field = None
    for pos,keyargpair in enumerate(keyargpairs):
        if "=" not in keyargpair:
            current_field = keyargpair
            if current_field in keyargdict:
                current_field = current_field + "-" + str(pos)
            
            keyargdict[current_field] = {}
        else:
            key, arg = keyargpair.split("=")
            keyargdict[current_field][key] = float(arg)

    return keyargdict

def check_inputs_non_neg(
    input: float,
) -> None:
    """Check that the input is a float and non-negative"""
    if not isinstance(input, float):
        raise TypeError(f"Input must be a float: {input}")
    
    if input < 0:
        raise ValueError(f"Input must be non-negative: {input}")
    
def check_inputs(
    input: float,
) -> None:
    """Check that the input is a float and non-negative"""
    if not isinstance(input, float):
        raise ValueError(f"Input must be a float: {input}")
    
### Potentials ###

def lj_cut(
    points: list[float], epsilon: float, sigma: float, cut: float
) -> list[float | None]:
    """Lennard-Jones potential with a cut-off at `cut`"""

    # Check inputs
    check_inputs_non_neg(epsilon)
    check_inputs_non_neg(sigma)
    check_inputs_non_neg(cut)

    values = []
    for r in points:
        if r <= cut:
            values.append(4 * epsilon * ((sigma / r) ** 12 - (sigma / r) ** 6))
        else:
            values.append(None)

    return values

def buck(
    points: list[float], A: float, rho: float, C: float
) -> list[float | None]:
    """Buckingham potential"""

    # Check inputs
    check_inputs_non_neg(A)
    check_inputs_non_neg(rho)
    check_inputs_non_neg(C)

    values = []
    for r in points:
        values.append(A * math.exp(-r/rho) - (C / r**6))

    return values

def buck_coul(
    points: list[float], A: float, rho: float, C: float, 
    q1: float = 1.0, q2: float = -1.0
) -> list[float | None]:
    """Buckingham potential with Coulombic term"""

    # Check inputs
    check_inputs_non_neg(A)
    check_inputs_non_neg(rho)
    check_inputs_non_neg(C)
    check_inputs(q1)
    check_inputs(q2)

    values = []
    for r in points:
        values.append(A * math.exp(-r/rho) - C / r**6 +
                      q1*q2/(r))
        
    # print(min(values))
    # print(max(values))

    return values