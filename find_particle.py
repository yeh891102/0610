import cv2
import numpy as np
import easygui

# Define the opening function
def Opening(image):
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    return opening

# Use EasyGUI to select the image file
image_path = easygui.fileopenbox(msg="Select an image file", title="Open Image", default="*.jpg", filetypes=["*.jpg", "*.png", "*.jpeg"])

# thr = 110
# open_num = 8
# thr_width = 30
if image_path:
    user_input = easygui.multenterbox(msg="Enter values for threshold, opening iterations, and width threshold", title="Input Parameters",
                                      fields=["Threshold (thr)", "Opening Iterations (open_num)", "Width Threshold (thr_width)"], 
                                      values=["110", "8", "30"])

    if user_input:
        try:
            thr = int(user_input[0])
            open_num = int(user_input[1])
            thr_width = int(user_input[2])
        except ValueError:
            easygui.msgbox("Please enter valid integer values for all parameters.", title="Input Error")
            exit()

        print(f"Selected file path: {image_path}")
        print(f"Threshold: {thr}, Opening Iterations: {open_num}, Width Threshold: {thr_width}")

        # Read the image
        image2 = cv2.imread(image_path)

        # Check if the image was successfully read
        if image2 is None:
            print("Error: Could not read the image.")
        else:
            # Convert to grayscale
            image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

            # Apply threshold
            _, image2_thr = cv2.threshold(image2, thr, 255, cv2.THRESH_BINARY)

            # Apply opening operation multiple times
            for i in range(open_num):
                image2_thr = Opening(image2_thr)

            # Find all connected components (white areas)
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(image2_thr)
            color_image2 = cv2.cvtColor(image2_thr, cv2.COLOR_GRAY2BGR)

            count_width = 0
            for i in range(1, num_labels):  # Skip the background
                width = stats[i, cv2.CC_STAT_WIDTH]
                if width > thr_width:
                    count_width += 1
                    x, y, w, h = stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP], width, stats[i, cv2.CC_STAT_HEIGHT]
                    cv2.rectangle(color_image2, (x, y), (x + w, y + h), (0, 255, 0), 2)

            print(image2.shape)
            print('count_width = ', count_width)

            # Display the images
            cv2.imshow('image2', image2)
            cv2.imshow('image2_thr', image2_thr)
            cv2.imshow('color_image2', color_image2)

            cv2.waitKey(0)
            cv2.destroyAllWindows()
    else:
        print("No input provided")
else:
    print("No file selected")