import cv2
import numpy as np

def ending_detect(video):
    video_input = cv2.VideoCapture(f"{video}")
    frame_number = 0

    while video_input.isOpened():
        frame_number = frame_number + 1
        success, frame_input = video_input.read()

        # if frame is read correctly success is True, function returns false if no ending is detected
        if not success:
            return {"detected": False}

        image_hsv = cv2.cvtColor(frame_input, cv2.COLOR_BGR2HSV)

        # the hue, saturation and value of the tiktok pixels after changing from bgr to hsv
        hue_of, saturation_of, value_of = 120, 121, 26
        detection_tolerance = 10

        #setting up the tolerances, bigger for saturation and value
        lower_bound = np.array([hue_of - detection_tolerance, saturation_of - detection_tolerance - 10, value_of - detection_tolerance - 10])
        upper_bound = np.array([hue_of + detection_tolerance, saturation_of + detection_tolerance + 10, value_of + detection_tolerance + 10])

        mask = cv2.inRange(image_hsv, lower_bound, upper_bound)
        mask_pixels = cv2.countNonZero(mask)
        total_pixels = frame_input.shape[0] * frame_input.shape[1]

        percentage_of = (mask_pixels / total_pixels) * 100

        if percentage_of > 25:
            return {"detected": True, "frames": frame_number - 1}
