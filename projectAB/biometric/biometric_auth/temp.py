import cv2
import os
import numpy as np
image_path=r"C:\Users\VICTUS\projectAB\biometric\biometric_auth\static\style\images\1__M_Right_middle_finger.BMP"


def loadimg():
    image=cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # cv2.imshow("image",image)
    save_path = os.path.join(os.path.dirname(__file__), 'static', 'style', 'images', 'processed_image.png')
    # cv2.imwrite(save_path, image)
    return image

# from google.colab.patches import cv2_imshow  # For displaying images in Colab

def divide_into_quadrants(image_path, grid_size=(2, 2)):
    
    """
    Divide a fingerprint image into quadrants.

    Args:
        image_path (str): Path to the fingerprint image.
        grid_size (tuple): Number of rows and columns in the grid.

    Returns:
        list: List of cropped image quadrants.
    """
    # Load the fingerprint image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Could not load image. Check the file path.")

    # Get image dimensions
    height, width = image.shape

    # Calculate quadrant size
    quad_height = height // grid_size[0]
    quad_width = width // grid_size[1]

    quadrants = []
    for row in range(grid_size[0]):
        for col in range(grid_size[1]):
            # Calculate coordinates for cropping
            start_x = col * quad_width
            start_y = row * quad_height
            end_x = start_x + quad_width
            end_y = start_y + quad_height

            # Crop the image
            quadrant = image[start_y:end_y, start_x:end_x]
            quadrants.append(quadrant)

    return quadrants

# Use the uploaded file
uploaded={r"C:\Users\VICTUS\projectAB\biometric\biometric_auth\static\style\images\1__M_Right_middle_finger.BMP": "metadata"}
uploaded_file_path = list(uploaded.keys())[0]

# Divide the fingerprint image into quadrants
quadrants = divide_into_quadrants(uploaded_file_path, grid_size=(3, 3))

# Display the quadrants
for i, quad in enumerate(quadrants):
    print(f"Quadrant {i+1}:")
    # Display the quadrant
    save_quad = os.path.join(os.path.dirname(__file__), 'static', 'quad', 'images', f'quadrant_{i+1}.png')
    cv2.imwrite(save_quad, quad)    
