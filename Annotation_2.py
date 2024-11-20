# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 18:35:23 2024

@author: UOU
"""

import cv2, os
import numpy as np
import glob

# Parameters for drawing
drawing = False  # True if the mouse is pressed
ix, iy = -1, -1  # Initial x, y coordinates of the region

# List to store segmentation points
annotations = []

# Mouse callback function to draw contours
def draw_contour(event, x, y, flags, param):
    global ix, iy, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        annotations.append([(x, y)])  # Start a new contour

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # Add points to the current contour
            annotations[-1].append((x, y))

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # Close the contour by connecting the last point to the first
        annotations[-1].append((x, y))

# Function to display the image and collect annotations
def segment_image(image_path):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Image not found: {image_path}")
        return

    # Create a clone of the image for annotation display
    annotated_image = image.copy()
    cv2.namedWindow("Image Segmentation")
    cv2.setMouseCallback("Image Segmentation", draw_contour)

    while True:
        # Show the annotations on the cloned image
        temp_image = annotated_image.copy()
        for contour in annotations:
            points = np.array(contour, dtype=np.int32)
            cv2.polylines(temp_image, [points], isClosed=True, color=(0, 255, 0), thickness=2)

        # Display the image with annotations
        cv2.imshow("Image Segmentation", temp_image)
        
        # Press 's' to save annotations, 'c' to clear, and 'q' to quit
        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            # Save annotations
            annotation_file = os.path.splitext(image_path)[0] + "_annotations.txt"
            with open(annotation_file, "w") as f:
                for contour in annotations:
                    f.write(str(contour) + "\n")
            print(f"Annotations saved to {annotation_file}")
        elif key == ord("c"):
            # Clear annotations
            annotations.clear()
            annotated_image = image.copy()
            print("Annotations cleared")
        elif key == ord("q"):
            break

    cv2.destroyAllWindows()

# Function to process all images in a directory
def process_images(directory, extensions=["jpg", "png"]):
    # Collect all image files from the directory
    image_files = []
    for ext in extensions:
        image_files.extend(glob.glob(os.path.join(directory, f"*.{ext}")))

    if not image_files:
        print("No image files found in the directory!")
        return

    # Process each image file
    for image_file in image_files:
        print(f"Processing: {image_file}")
        segment_image(image_file)

    print("All images processed!")

# Example usage
if __name__ == "__main__":
    # Specify the directory containing images
    image_directory = r"C:/Users/cic/Downloads/Repo-master/Image_dataset"

    # Process all images in the directory
    process_images(image_directory, extensions=["jpg", "png"])
