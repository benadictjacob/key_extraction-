import cv2
import numpy as np
from scipy import ndimage
from typing import List, Tuple
import os
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from .test6 import extract_all_keys ,calculate_similarity
class FingerprintMinutiae:
    def __init__(self, image_path: str):
        """Initialize with path to fingerprint image."""
        self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if self.image is None:
            raise ValueError(f"Could not load image at {image_path}")
        self.height, self.width = self.image.shape
        self.binary_image = None
        self.skeleton = None
        self.debug_images = {}
        
    def preprocess(self, debug: bool = False) -> None:
        """Preprocess the fingerprint image."""
        # Save original image for debugging
        if debug:
            self.debug_images['original'] = self.image.copy()
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(self.image, (5, 5), 0)
        if debug:
            self.debug_images['blurred'] = blurred.copy()
        
        # Apply adaptive thresholding
        self.binary_image = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        if debug:
            self.debug_images['binary'] = self.binary_image.copy()
        
        # Remove noise using morphological operations
        kernel = np.ones((3,3), np.uint8)
        self.binary_image = cv2.morphologyEx(self.binary_image, cv2.MORPH_OPEN, kernel)
        if debug:
            self.debug_images['opened'] = self.binary_image.copy()
            
        self.binary_image = cv2.morphologyEx(self.binary_image, cv2.MORPH_CLOSE, kernel)
        if debug:
            self.debug_images['closed'] = self.binary_image.copy()
        
        # Skeletonize the image
        self.skeleton = self._skeletonize(self.binary_image)
        if debug:
            self.debug_images['skeleton'] = self.skeleton.copy()
    
    def _skeletonize(self, image: np.ndarray) -> np.ndarray:
        """Skeletonize the binary image using Zhang-Suen algorithm."""
        # Ensure image is binary (0 and 255)
        binary = (image > 0).astype(np.uint8) * 255
        
        # Use OpenCV's skeletonization for better performance
        try:
            skeleton = cv2.ximgproc.thinning(binary)
        except:
            skeleton = None
            
        # If OpenCV's skeletonization is not available, use our implementation
        if skeleton is None:
            skeleton = self._zhang_suen_skeletonize(binary)
            
        return skeleton
    
    def _zhang_suen_skeletonize(self, image: np.ndarray) -> np.ndarray:
        """Skeletonize the binary image using Zhang-Suen algorithm."""
        # Convert to binary (0 and 1)
        binary = (image > 0).astype(np.uint8)
        skeleton = binary.copy()
        
        while True:
            # First subiteration
            skeleton = self._zhang_suen_iteration(skeleton, 1)
            # Second subiteration
            skeleton = self._zhang_suen_iteration(skeleton, 2)
            # Check if any changes were made
            if not np.any(skeleton != binary):
                break
            binary = skeleton.copy()
            
        # Convert back to 0 and 255
        return skeleton.astype(np.uint8) * 255
    
    def _zhang_suen_iteration(self, image: np.ndarray, subiteration: int) -> np.ndarray:
        """One iteration of Zhang-Suen thinning algorithm."""
        output = image.copy()
        height, width = image.shape
        
        for i in range(1, height-1):
            for j in range(1, width-1):
                if image[i,j] == 0:
                    continue
                    
                # Get 8-neighbors
                p2, p3, p4, p5, p6, p7, p8, p9 = self._get_neighbors(image, i, j)
                
                # Calculate number of black-white transitions
                transitions = sum([p2 != p3, p3 != p4, p4 != p5, p5 != p6,
                                 p6 != p7, p7 != p8, p8 != p9, p9 != p2])
                
                # Calculate number of black neighbors
                black_neighbors = sum([p2, p3, p4, p5, p6, p7, p8, p9])
                
                if subiteration == 1:
                    if (2 <= black_neighbors <= 6 and transitions == 1 and
                        p2 * p4 * p6 == 0 and p4 * p6 * p8 == 0):
                        output[i,j] = 0
                else:
                    if (2 <= black_neighbors <= 6 and transitions == 1 and
                        p2 * p4 * p8 == 0 and p2 * p6 * p8 == 0):
                        output[i,j] = 0
                        
        return output
    
    def _get_neighbors(self, image: np.ndarray, i: int, j: int) -> Tuple[int, ...]:
        """Get 8-neighbors of a pixel."""
        return (image[i-1,j], image[i-1,j+1], image[i,j+1], image[i+1,j+1],
                image[i+1,j], image[i+1,j-1], image[i,j-1], image[i-1,j-1])
    
    def extract_minutiae(self) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        """Extract minutiae points from the skeletonized image."""
        endpoints = []
        bifurcations = []
        
        # Ensure skeleton is binary (0 and 255)
        skeleton = (self.skeleton > 0).astype(np.uint8) * 255
        
        for i in range(1, self.height-1):
            for j in range(1, self.width-1):
                if skeleton[i,j] == 0:
                    continue
                    
                # Get 8-neighbors
                neighbors = self._get_neighbors(skeleton, i, j)
                black_neighbors = sum([n > 0 for n in neighbors])
                
                # Endpoint detection (1 black neighbor)
                if black_neighbors == 1:
                    endpoints.append((i, j))
                    
                # Bifurcation detection (3 black neighbors)
                elif black_neighbors == 3:
                    bifurcations.append((i, j))
                    
        return endpoints, bifurcations
    
    def visualize_minutiae(self, endpoints: List[Tuple[int, int]], 
                          bifurcations: List[Tuple[int, int]], 
                          output_path: str = None) -> np.ndarray:
        """Visualize the extracted minutiae points."""
        # Convert skeleton to RGB for visualization
        visualization = cv2.cvtColor(self.skeleton, cv2.COLOR_GRAY2RGB)
        
        # Draw endpoints in blue
        for i, j in endpoints:
            cv2.circle(visualization, (j, i), 3, (255, 0, 0), -1)
            
        # Draw bifurcations in red
        for i, j in bifurcations:
            cv2.circle(visualization, (j, i), 3, (0, 0, 255), -1)
            
        if output_path:
            cv2.imwrite(output_path, visualization)
            
        return visualization
    
    def plot_minutiae_2d(self, endpoints: List[Tuple[int, int]], 
                         bifurcations: List[Tuple[int, int]], 
                         output_path: str = None) -> None:
        """Plot minutiae points on a 2D graph."""
        plt.figure(figsize=(10, 10))
        
        # Plot endpoints
        if endpoints:
            y_endpoints, x_endpoints = zip(*endpoints)
            plt.scatter(x_endpoints, y_endpoints, c='blue', marker='o', s=50, label='Endpoints')
        
        # Plot bifurcations
        if bifurcations:
            y_bifurcations, x_bifurcations = zip(*bifurcations)
            plt.scatter(x_bifurcations, y_bifurcations, c='red', marker='o', s=50, label='Bifurcations')
        
        # Set axis labels and title
        plt.xlabel('X-axis (pixels)')
        plt.ylabel('Y-axis (pixels)')
        plt.title('Minutiae Points Distribution')
        plt.legend()
        
        # Invert y-axis to match image coordinates
        plt.gca().invert_yaxis()
        
        # Add grid
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Save the plot if output path is provided
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        
        # Show the plot
        plt.show()
    
    def save_debug_images(self, output_dir: str) -> None:
        """Save debug images to the specified directory."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        for name, image in self.debug_images.items():
            cv2.imwrite(os.path.join(output_dir, f"{name}.jpg"), image)
            
            
def convert_to_key(file_path: str) -> None:
    """Convert fingerprint image to key."""
    fingerprint = FingerprintMinutiae(file_path)
    fingerprint.preprocess(debug=True)
    
    # Extract minutiae points
    endpoints, bifurcations = fingerprint.extract_minutiae()
    all_points = endpoints + bifurcations
    minuetes=np.array(all_points)
    combined_keys = extract_all_keys(minuetes)
    return combined_keys
    # Visualize minutiae points
    # visualization = fingerprint.visualize_minutiae(endpoints, bifurcations)
    
    # Save visualization
    # output_path = os.path.splitext(file_path)[0] + "_minutiae.jpg"
    # cv2.imwrite(output_path, visualization)
    
    # Plot minutiae points in 2D
    # fingerprint.plot_minutiae_2d(endpoints, bifurcations, output_path=os.path.splitext(file_path)[0] + "_minutiae_plot.jpg")
    
    # Save debug images
    # fingerprint.save_debug_images(output_dir=os.path.dirname(file_path))
    
    
    