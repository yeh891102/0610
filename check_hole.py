import cv2
import numpy as np
import easygui

def Opening(image):
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    return opening

image_path = easygui.fileopenbox(msg="Select an image file", title="Open Image", default="*.jpg", filetypes=["*.jpg", "*.png", "*.jpeg"])

if image_path:
    print(f"Selected file path: {image_path}")
    # Read the image
    image3 = cv2.imread(image_path)

    # Check if the image was successfully read
    if image3 is None:
        print("Error: Could not read the image.")
    else:
        image3 = cv2.cvtColor(image3, cv2.COLOR_BGR2GRAY)
        _, image3_thr = cv2.threshold(image3, 180, 255, cv2.THRESH_BINARY)
        for i in range(1):
            image3_thr = Opening(image3_thr)
        num_labels, labels = cv2.connectedComponents(image3_thr)
        num_white_components = num_labels - 1

        cv2.imshow('image3', image3)
        cv2.imshow('image3_thr', image3_thr)
        cv2.waitKey(0)
        