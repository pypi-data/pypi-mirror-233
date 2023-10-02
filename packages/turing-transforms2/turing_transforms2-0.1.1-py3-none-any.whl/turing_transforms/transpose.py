"""Implementation of 2D transpose function for floats."""


def transpose2d(input_matrix: list[list[float]]) -> list:
    """Transposed 2-dimensional matrix.

    Inner lists are considered rows of the matrix.

    Args:
        input_matrix: input list.

    Returns:
        list: with axis permuted.
    """
    # Return an empty list if the input matrix is empty
    if not input_matrix or not input_matrix[0]:
        return []
    transposed_matrix = []
    n_cols = len(input_matrix[0])
    n_rows = len(input_matrix)
    for col in range(n_cols):
        new_row = []
        for row in range(n_rows):
            new_row.append(input_matrix[row][col])
        transposed_matrix.append(new_row)
    return transposed_matrix
