#!/usr/bin/env python3

import cv2
import numpy as np

# Load the image
image = cv2.imread('ula.jpg')
h, w = image.shape[:2]  # Get the height and width of the original image


# Define the four corner points in the distorted image (order: top-left, top-right, bottom-right, bottom-left)
distorted_pts = np.array([
    [ 444,  439],  # Top-left corner
    [9653,  431],  # Top-right corner
    [9663, 8764],  # Bottom-right corner
    [440,  8772]   # Bottom-left corner
], dtype=np.float32)

# Define where those points should map in the undistorted image
desired_pts = np.array([
    [444,        439       ],  # New Top-left
    [444 + 9209, 439       ],  # New Top-right
    [444 + 9209, 439 + 8333],  # New Bottom-right
    [444,        439 + 8333]   # New Bottom-left
], dtype=np.float32)

# Compute the perspective transformation matrix
matrix = cv2.getPerspectiveTransform(distorted_pts, desired_pts)

# Apply the perspective warp
corrected_image = cv2.warpPerspective(image, matrix, (w, h))

# Save and show the corrected image
cv2.imwrite('ula-rectified.jpg', corrected_image)

