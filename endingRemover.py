import ffmpeg
import os
import shutil
from ffmpeg import overwrite_output


class ConversionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class RemovalError(Exception):
    def __init__(self, message):
        super.__init__(message)

def end_remove(video, frame_number, video_extension, keep_original):
    frame_raw = ""
    video_name = video[:-len(video_extension)]

    video_input = shutil.copy2(f"{video}", f"{video_name}_original{video_extension}")
    try:
        os.remove(video)
    except PermissionError as e:
        raise RemovalError("Not enough permissions to manage your files!") from e

    probe_data = ffmpeg.probe(f"{video_input}")
    video_stream = probe_data["streams"]
    for stream in video_stream:
        if stream["codec_type"] == "video":
            frame_raw = stream["r_frame_rate"]
            break
    numerator_str, denominator_str = frame_raw.split("/")
    frame_rate = float(numerator_str) / float(denominator_str)
    calculated_timestamp = frame_number / frame_rate

    try:
        result_of_conversion = ffmpeg.input(f"{video_input}", ss = "0", to = f"{calculated_timestamp}").output(f"{video}", c = "copy").run(overwrite_output=True)
        if not keep_original:
            os.remove(video_input)
        return result_of_conversion
    except ffmpeg.Error as e:
        raise ConversionError(f"{e}")