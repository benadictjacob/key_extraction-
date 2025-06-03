import numpy as np
import cv2
import math
from Levenshtein import distance as levenshtein_distance
from typing import List

#extract keypoints
def extract_keypoints(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    blurred_img = cv2.GaussianBlur(img, (5, 5), 0)
    binary_img = cv2.adaptiveThreshold(blurred_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    def skeletonize(image):
        size = np.size(image)
        skel = np.zeros(image.shape, np.uint8)
        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        done = False
        while not done:
            eroded = cv2.erode(image, element)
            temp = cv2.dilate(eroded, element)
            temp = cv2.subtract(image, temp)
            skel = cv2.bitwise_or(skel, temp)
            image = eroded.copy()
            zeros = size - cv2.countNonZero(image)
            if zeros == size:
                done = True
        return skel

    skeleton = skeletonize(binary_img)
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(skeleton, None)
    keypoint_coords = np.array([keypoint.pt for keypoint in keypoints], dtype=np.float32)
    return keypoint_coords

#the extract function
def extract_all_keys(keypoint_coords: np.ndarray) -> str:
    keys = []  # List to store all generated keys
    for a in range(len(keypoint_coords)):
        # Extract four points
        x1, y1 = keypoint_coords[a]  # Current point

        # Use modulo to wrap around the list if indices exceed its length
        x2, y2 = keypoint_coords[(a + 45) % len(keypoint_coords)]  # Point at index (a + 45)
        x3, y3 = keypoint_coords[(a + 90) % len(keypoint_coords)]  # Point at index (a + 90)
        x4, y4 = keypoint_coords[(a + 135) % len(keypoint_coords)]  # Point at index (a + 135)

        # Compute distances
        d12 = int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
        d23 = int(math.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2))
        d34 = int(math.sqrt((x3 - x4) ** 2 + (y3 - y4) ** 2))
        d41 = int(math.sqrt((x4 - x1) ** 2 + (y4 - y1) ** 2))

        # Check if distances are valid
        if d12 != 0 and d23 != 0 and d34 != 0 and d41 != 0:
            # Compute intermediate values and angles
            i12 = ((d23 ** 2) + (d34 ** 2) + (d41 ** 2) - (d12 ** 2)) / (2 * d23 * d34 * d41)
            i23 = ((d34 ** 2) + (d12 ** 2) + (d41 ** 2) - (d23 ** 2)) / (2 * d34 * d12 * d41)
            i34 = ((d12 ** 2) + (d23 ** 2) + (d41 ** 2) - (d34 ** 2)) / (2 * d23 * d12 * d41)
            i41 = ((d12 ** 2) + (d23 ** 2) + (d34 ** 2) - (d41 ** 2)) / (2 * d23 * d12 * d34)

            # Clamp intermediate values
            i12 = max(min(i12, 1), -1)
            i23 = max(min(i23, 1), -1)
            i34 = max(min(i34, 1), -1)
            i41 = max(min(i41, 1), -1)

            # Compute angles
            t12 = float(180 - (math.acos(i12) * (180 / math.pi)))
            t23 = float(180 - (math.acos(i23) * (180 / math.pi)))
            t34 = float(180 - (math.acos(i34) * (180 / math.pi)))
            t41 = float(180 - (math.acos(i41) * (180 / math.pi)))

            # Adjust angles
            al12 = float((math.atan2((y1 - y2), (x1 - x2))) - t12)
            al23 = float((math.atan2((y2 - y3), (x2 - x3))) - t23)
            al34 = float((math.atan2((y3 - y4), (x3 - x4))) - t34)
            al41 = float((math.atan2((y4 - y1), (x4 - x1))) - t41)

            # Generate a key
            sv = f"{d12}_{d23}_{d34}_{d41}_{al12}_{al23}_{t34}_{t41}"
            keys.append(sv)  # Add the key to the list

    # Combine all keys into a single string
    combined_keys = "\n".join(keys)  # Use newline as a separator
    return combined_keys  # Return the combined string

def calculate_similarity(str1, str2):
    lev_distance = levenshtein_distance(str1, str2)
    max_len = max(len(str1), len(str2))
    similarity_percentage = (1 - lev_distance / max_len) * 100
    print(similarity_percentage)
    return similarity_percentage

# Paths to the fingerprint images
if __name__ == "__main__":
    image_path1 = r'biometricauth\SOCOFing\Real\2__F_Left_thumb_finger.BMP'
    image_path2 = r'biometricauth\SOCOFing\Real\2__F_Left_thumb_finger.BMP'

    # Extract keypoints
    keypoint_coords1 = extract_keypoints(image_path1)
    keypoint_coords2 = extract_keypoints(image_path2)

    # Ensure the indices are within the valid range
    if len(keypoint_coords1) == 0 or len(keypoint_coords2) == 0:
        raise ValueError("No keypoints found in one or both images.")

    # Generate keys for both sets of keypoints
    keys1 = extract_all_keys(keypoint_coords1)
    keys2 = extract_all_keys(keypoint_coords2)

    # Calculate similarity percentage
    similarity_percentage = calculate_similarity(keys1, keys2)
    print(f"Similarity percentage: {similarity_percentage:.2f}%")

    # Check if the similarity percentage is greater than or equal to 90%
    if similarity_percentage >= 90:
        print("The fingerprints are similar.")
    else:
        print("The fingerprints are not similar.")





