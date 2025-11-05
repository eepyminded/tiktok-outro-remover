import cv2
import matplotlib.pyplot as plt
import numpy as np

def endingDetecter(video):
    videoInput = cv2.VideoCapture(f"{video}")
    frameNumber = 0

    while videoInput.isOpened():
        frameNumber = frameNumber + 1
        success, frameInput = videoInput.read()

        # if frame is read correctly success is True, function returns false if no ending is detected
        if not success:
            return False

        imageHsv = cv2.cvtColor(frameInput, cv2.COLOR_BGR2HSV)

        # the hue, saturation and value of the tiktok pixels after changing from bgr to rgb
        hueOf, saturationOf, valueOf = 120, 121, 26
        detectionTolerance = 10 

        #setting up the tolerances, bigger for saturation and value
        lowerBound = np.array([hueOf - detectionTolerance, saturationOf - detectionTolerance - 10, valueOf - detectionTolerance - 10])
        upperBound = np.array([hueOf + detectionTolerance, saturationOf + detectionTolerance + 10, valueOf + detectionTolerance + 10])

        mask = cv2.inRange(imageHsv, lowerBound, upperBound)
        maskPixels = cv2.countNonZero(mask)
        totalPixels = frameInput.shape[0] * frameInput.shape[1]

        percentageOf = (maskPixels / totalPixels) * 100

        if percentageOf > 25:
            return frameNumber
