import cv2
import numpy as np
import easyocr

# model init for detecting text
reader = easyocr.Reader(['en'], download_enabled=False, model_storage_directory="models", verbose=False)

def ending_detect(video):
    video_input = cv2.VideoCapture(f"{video}")

    detected_frames = 0

    # the hue, saturation and value of the tiktok pixels after changing from bgr to hsv
    hue_of, saturation_of, value_of = 120, 121, 26

    # setting up the tolerances, bigger for saturation and value
    detection_tolerance = 10

    lower_bound = np.array([hue_of - detection_tolerance, saturation_of - detection_tolerance - 5, value_of - detection_tolerance - 5])
    upper_bound = np.array([hue_of + detection_tolerance, saturation_of + detection_tolerance + 5, value_of + detection_tolerance + 5])

    # starting to look from the last 5 seconds
    fps = video_input.get(cv2.CAP_PROP_FPS)
    print(f"fps: {fps}")
    total_frames = int(video_input.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"total_frames: {total_frames}")
    start_frame = max(0, total_frames - int(fps * 5))
    print(f"calculated start frame: {start_frame}")
    video_input.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    frame_number = start_frame

    width_video = video_input.get(cv2.CAP_PROP_FRAME_WIDTH)
    height_video = video_input.get(cv2.CAP_PROP_FRAME_HEIGHT)
    total_pixels = width_video * height_video

    while video_input.isOpened():
        frame_number = frame_number + 1
        success, frame_input = video_input.read()

        # if frame is read correctly success is True, function returns false if no ending is detected
        if not success:
            break

        frame_hsv = cv2.cvtColor(frame_input, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(frame_hsv, lower_bound, upper_bound)
        mask_pixels = cv2.countNonZero(mask)

        percentage_of = (mask_pixels / total_pixels) * 100

        # 3 consecutive frames needs to be detected before deeming the frame to start with an outro
        if percentage_of > 25 or word_detect(frame_input, "tiktok"):
            detected_frames += 1
        else:
            detected_frames = 0

        if detected_frames == 3:
            return {"detected": True, "frames": frame_number - detected_frames}
    return {"detected": False}


def word_detect(frame_input, word):
    # only checking at around the center so the moving watermarks arent caught up in the ocr
    video_height, video_width = frame_input.shape[:2]

    width_bottom = int(video_width * 0.25)
    width_top = int(video_width * 0.75)

    height_bottom = int(video_height * 0.25)
    height_top = int(video_height * 0.75)

    center_crop = frame_input[width_bottom:width_top, height_bottom:height_top]

    frame_gray = cv2.cvtColor(center_crop, cv2.COLOR_BGR2GRAY)
    text_in_image = reader.readtext(frame_gray, detail=0)

    for text in text_in_image:
        clean_text = text.lower().replace(" ", "")
        if word in clean_text:
            return True
        
    return False