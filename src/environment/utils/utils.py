import math
from typing import Union

def sign(x):
    return math.copysign(1, x)


def clamp(val: Union[float, int], min_val: Union[float, int], max_val: Union[float, int]):
    if val < min_val:
        return min_val
    elif val > max_val:
        return max_val
    else:
        return val