import cv2
import numpy as np
from sklearn.cluster import KMeans

# Define a dictionary of common colors
COLOR_NAMES = {
    (255, 0, 0): "Red", (0, 255, 0): "Green", (0, 0, 255): "Blue",
    (255, 255, 0): "Yellow", (0, 255, 255): "Cyan", (255, 0, 255): "Magenta",
    (128, 0, 0): "Maroon", (128, 128, 0): "Olive", (0, 128, 0): "Dark Green",
    (0, 128, 128): "Teal", (0, 0, 128): "Navy", (128, 0, 128): "Purple",
    (192, 192, 192): "Silver", (128, 128, 128): "Gray", (0, 0, 0): "Black",
    (255, 255, 255): "White"
}

def closest_color(rgb):
    """Find the closest color from the COLOR_NAMES dictionary."""
    min_distance = float("inf")
    closest_name = "Unknown"
    for key, name in COLOR_NAMES.items():
        distance = np.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, key)))
        if distance < min_distance:
            min_distance = distance
            closest_name = name
    return closest_name

def detect_color_kmeans(image, x1, y1, x2, y2, clusters=5, min_size=10):
    """Detects the dominant color using K-Means clustering with error handling."""
    # Ensure bounding box is within image dimensions
    height, width, _ = image.shape
    if x1 < 0 or y1 < 0 or x2 > width or y2 > height:
        return "Error: Bounding box out of image bounds"

    # Ensure bounding box is large enough
    if (x2 - x1) < min_size or (y2 - y1) < min_size:
        return "Error: Bounding box too small"

    roi = image[y1:y2, x1:x2]
    roi = roi.reshape((-1, 3))

    # Ensure we have enough pixels for clustering
    if roi.shape[0] < clusters:
        return "Error: Not enough pixels for K-Means"

    try:
        kmeans = KMeans(n_clusters=clusters, n_init=10)
        kmeans.fit(roi)
        dominant_color = kmeans.cluster_centers_[np.argmax(np.bincount(kmeans.labels_))]

        # Convert to closest color name
        color_name = closest_color(dominant_color.astype(int))
        return color_name
    except Exception as e:
        return f"Error: {str(e)}"
