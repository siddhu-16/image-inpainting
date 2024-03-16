import cv2
import numpy as np
from skimage import color, util, feature

def convert_to_gray(image, damaged_mask):
    # Convert the image to grayscale
    gray_image = color.rgb2gray(image)

    # Apply the damaged area mask
    damaged_gray_image = np.copy(gray_image)
    damaged_gray_image[damaged_mask] = 0  # Set damaged area to black

    return damaged_gray_image

def compute_glcm_and_contrast(gray_image, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4]):
    # Normalize the image to integer values between 0 and 255
    gray_image = util.img_as_ubyte(gray_image)

    # Compute the GLCM
    glcm = feature.greycomatrix(gray_image, distances=distances, angles=angles, symmetric=True, normed=True)

    # Compute contrast as a measure of texture
    contrast = feature.greycoprops(glcm, 'contrast')

    return contrast

# Example usage:
# Load your image
image = cv2.imread("/image1.jpg")

# Assuming you have a binary mask for the damaged area (white pixels indicating damaged area)
mask = cv2.imread("/mask1.png", cv2.IMREAD_GRAYSCALE)

# Convert the damaged area to grayscale
damaged_gray_image = convert_to_gray(image, mask)

# Compute GLCM and contrast
contrast = compute_glcm_and_contrast(damaged_gray_image)

# Display the results
cv2.imshow("Original Image", image)
cv2.imshow("Damaged Area in Grayscale", damaged_gray_image)
print("Contrast:", contrast)
cv2.waitKey(0)
cv2.destroyAllWindows()
