"""Implements 2D convolution only with a stride parameter."""

import numpy as np


def convolution2d(
    input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1
) -> np.ndarray:
    """2D convolution operator. Channel dimension is not supported.

    Args:
        input_matrix: of dims (rows, cols).
        kernel: of dims (rows, cols)
        stride: kernel shift size.
    Returns:
        numpy array.
    """
    # Get the dimensions of the input and the kernel
    input_rows, input_cols = input_matrix.shape
    kernel_rows, kernel_cols = kernel.shape

    # Calculate the size of the output matrix
    output_rows = (input_rows - kernel_rows) // stride + 1
    output_cols = (input_cols - kernel_cols) // stride + 1

    # Initialize the output matrix with zeros
    output_matrix = np.zeros((output_rows, output_cols))

    for i in range(0, output_rows):
        for j in range(0, output_cols):
            # Extract the relevant sub-matrix from the input matrix
            sub_matrix = input_matrix[
                i * stride : i * stride + kernel_rows,
                j * stride : j * stride + kernel_cols,
            ]

            # Multiply the sub-matrix with the kernel and sum the results
            result = np.sum(sub_matrix * kernel)

            # Assign the result to the output matrix
            output_matrix[i, j] = result

    return output_matrix
