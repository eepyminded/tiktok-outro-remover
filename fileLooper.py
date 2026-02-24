import os

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

def files_count(directory):
    if not isinstance(directory, str):
        raise NotStringError(directory)

    if not os.access(directory, os.F_OK):
        raise InvalidPathError(directory)

    if not os.access(directory, os.R_OK) or not os.access(directory, os.W_OK):
        raise PermissionError(f"ERROR: Not enough permissions to manage files in {directory} dir!")

    file_amount = 0

    for file in os.listdir(directory):
        file_amount += 1

    return file_amount

def loop_through_files(directory, keep_original_video, keep_has_original_in, progress_queue, same_output_dir_var, output_dir, ignore_progress_queue = False):
    if not isinstance(directory, str):
        raise NotStringError(directory)

    if not os.access(directory, os.F_OK):
        raise InvalidPathError(directory)

    # check if we can read and write in input directory
    if not os.access(directory, os.R_OK) and not os.access(directory, os.W_OK):
        raise PermissionError(f"ERROR: Not enough permissions to manage files in chosen dir!")

    # if user wants other output dir, check also for its permissions
    if not same_output_dir_var and not os.access(output_dir, os.R_OK) and not os.access(output_dir, os.W_OK):
        raise PermissionError(f"ERROR: Not enough permissions to manage files in chosen dir!")

    # also we need to check if user wants the same output path as the input, or chosen by them
    if same_output_dir_var:
        output_dir = directory
    else:
        output_dir = output_dir

    files_only_name = []
    files_wth_path = []
    amount_of_files = 0

    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            files_only_name.append(file)
            files_wth_path.append(os.path.join(directory, file))
        else:
            continue

    video_with_ending_amount = 0
    video_amount = 0

    for file in files_wth_path:
        if file.endswith((".mp4", ".webm", ".mov", "mkv")):

            # we only want to inform user about the video type files in directory
            amount_of_files += 1
            if not ignore_progress_queue:
                progress_queue.put(amount_of_files)

            # check if it has *original* string in the file, if it does we skip the file (user choice)
            if keep_has_original_in and "original" in file:
                continue

            video_amount += 1
            split_file = os.path.splitext(file)
            video_extension = split_file[1]

            #using os to check permissions because opencv doesn't raise an exception when it can't open a file
            if not os.access(file, os.R_OK) or not os.access(file, os.W_OK):
                raise PermissionError(f"ERROR: Not enough permissions to read {file}")

            video_ending_info = endingDetecter.ending_detect(file)
            # no ending detected
            if not video_ending_info["detected"]:
                continue
            else:
                video_with_ending_amount += 1
                # we also pass files_only_name[amount_of_files - 1], which is only the name of the video without its path, we pass directory as our input path
                endingRemover.end_remove(file, video_ending_info["frames"], video_extension, keep_original_video, output_dir, files_only_name[amount_of_files - 1])
    if not ignore_progress_queue:
        progress_queue.put({"video_amount": video_amount, "video_with_ending_amount": video_with_ending_amount})
    return