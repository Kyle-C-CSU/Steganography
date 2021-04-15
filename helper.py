# Helper functions are placed here so as not to clutter main files

import numpy as np


# Converts various types of input data to a binary representation
def to_binary(data):

    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])

    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]

    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")

    else:
        raise TypeError("Type not supported.")