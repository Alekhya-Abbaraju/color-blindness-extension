import numpy as np

# Protanopia Matrix
protanopia_matrix = np.array([[0.567, 0.433, 0],
                              [0.558, 0.442, 0],
                              [0, 0.242, 0.758]])

# Deuteranopia Matrix
deuteranopia_matrix = np.array([[0.625, 0.375, 0],
                                [0.7, 0.3, 0],
                                [0, 0.3, 0.7]])

# Tritanopia Matrix
tritanopia_matrix = np.array([[0.95, 0.05, 0],
                              [0, 0.433, 0.567],
                              [0, 0.475, 0.525]])

# Dictionary to access each matrix easily
colorblind_matrices = {
    "protanopia": protanopia_matrix,
    "deuteranopia": deuteranopia_matrix,
    "tritanopia": tritanopia_matrix
}
