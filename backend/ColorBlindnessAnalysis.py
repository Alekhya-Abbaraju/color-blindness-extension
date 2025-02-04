import cv2
import numpy as np
from ColorMasks import colorblind_matrices

# Apply color blindness simulation matrix to image
def simulate_colorblindness(cb_simulation_matrix, image):
    return cv2.transform(image, cb_simulation_matrix)

# Process the image based on selected filter
def process_image(image_path, filter_name):
    image = cv2.imread(image_path)
    
    # Get the appropriate color blindness matrix
    cb_simulation_matrix = colorblind_matrices.get(filter_name)
    
    if cb_simulation_matrix is None:
        raise ValueError("Invalid color blindness filter")

    # Apply the color blindness simulation to the image
    cb_image = simulate_colorblindness(cb_simulation_matrix, image)
    
    # Convert the image back to RGB for proper display
    cb_image = cv2.cvtColor(cb_image, cv2.COLOR_BGR2RGB)
    
    return cb_image
