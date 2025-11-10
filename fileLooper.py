import os
from pyexpat.errors import messages

import endingDetecter
import endingRemover

class NotStringError(Exception):
    def __init__(self, var):
        super().__init__(self, var)
        self.var = var

class InvalidPathError(Exception):
    def __init__(self, path):
        super().__init__()
        self.path = path

def loop_through_files(directory,  keep_original_video):
    if not isinstance(directory, str):
        raise NotStringError(directory)

    if not os.access(directory, os.F_OK):
        raise InvalidPathError(directory)

    # check if we can read and write in that directory
    if not os.access(directory, os.R_OK) or not os.access(directory, os.W_OK):
        raise PermissionError(f"ERROR: Not enough permissions to manage files in {directory} dir!")

    files = []

    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            files.append(os.path.join(directory, file))
        else:
            continue

    video_with_ending_amount = 0
    video_amount = 0

    for file in files:
        if file.endswith((".mp4", ".webm", ".mov", "mkv")):
            video_amount += 1
            split_file = os.path.splitext(file)
            video_extension = split_file[1]

            #using os to check permissions because opencv doesn't raise an exception when it can't open a file
            if not os.access(file, os.R_OK) or not os.access(file, os.W_OK):
                raise PermissionError(f"ERROR: Not enough permissions to read {file}")

            video_ending_info = endingDetecter.ending_detect(file)
            print(video_ending_info)
            # no ending detected
            if not video_ending_info["detected"]:
                continue
            else:
                video_with_ending_amount += 1
                endingRemover.end_remove(file, video_ending_info["frames"], video_extension, keep_original_video)

    return {"video_amount": video_amount, "video_with_ending_amount": video_with_ending_amount}