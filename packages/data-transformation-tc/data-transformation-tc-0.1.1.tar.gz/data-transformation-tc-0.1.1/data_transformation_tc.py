import numpy as np

def transpose2d(input_matrix: list[list[float]]) -> list[list[float]]:
    """
    Transpose a 2D matrix.
    
    Parameters:
    - input_matrix: A list of lists of real numbers representing a 2D matrix.
    
    Returns:
    - A list of lists of real numbers representing the transposed 2D matrix.
    """
    transposed = [[row[i] for row in input_matrix] for i in range(len(input_matrix[0]))]
    return transposed

def window1d(input_array, size, shift=1, stride=1):
    """
    Generate windows for 1D array or list.
    
    Parameters:
    - input_array: A list or 1D numpy array of real numbers.
    - size: The window size.
    - shift: The shift (step size) between different windows.
    - stride: The stride (step size) within each window.
    
    Returns:
    - A list of lists or 1D numpy arrays of real numbers.
    """
    if not input_array:
        return []

    input_array = list(input_array)

    windows = []
    for start in range(0, len(input_array) - size + 1, shift):
        window = input_array[start:start + size:stride]
        windows.append(window)

    return windows

def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    """
    Compute the cross-correlation of a 2D input matrix with a kernel.

    Parameters:
    - input_matrix: A 2D numpy array.
    - kernel: A 2D numpy array.
    - stride: Stride value for the kernel.

    Returns:
    - A 2D numpy array of the result.
    """
    i_h, i_w = input_matrix.shape
    k_h, k_w = kernel.shape
    o_h = (i_h - k_h) // stride + 1
    o_w = (i_w - k_w) // stride + 1
    output = np.zeros((o_h, o_w))
    for x in range(0, i_h - k_h + 1, stride):
        for y in range(0, i_w - k_w + 1, stride):
            output[x // stride, y // stride] = np.sum(input_matrix[x:x+k_h, y:y+k_w] * kernel)
    return output

if __name__ == '__main__':
    # Sample test cases for each function
    matrix = [
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
        [7.0, 8.0, 9.0]
    ]
    print("Transpose Test:", transpose2d(matrix))
    
    input_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    window_size = 3
    window_shift = 2
    window_stride = 2
    print("Windowing Test:", window1d(input_data, window_size, window_shift, window_stride))
    
    input_matrix = np.array([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ])
    kernel = np.array([
        [1, 0],
        [0, -1]
    ])
    print("Convolution Test:", convolution2d(input_matrix, kernel, stride=2))
