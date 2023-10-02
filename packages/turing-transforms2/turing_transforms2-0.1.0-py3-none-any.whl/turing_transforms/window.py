"""Window1D implementation."""
import numpy as np


def window1d(
    input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1,
) -> list[list] | list[np.ndarray]:
    """Creates a windowed dataset from a 1D NumPy array.

    Function drops remainder and only includes full size windows.

    Args:
        input_array: list 1D numpy array.
        size: size of the sliding window.
        shift: number of positions the window
            is shifted to the right each iteration.
        stride: number of positions between elements in the window.
    Return:
        list of generated windows.
    """
    # Calculate the number of windows that can be created
    num_windows = (len(input_array) - size) // shift + 1

    windows = []

    for i in range(0, num_windows * shift, shift):
        window = input_array[i : i + size * stride : stride]
        windows.append(window)

    return windows
