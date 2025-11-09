import ffmpeg
import os
import shutil

class ConversionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class RemovalError(Exception):
    def __init__(self, message):
        super.__init__(message)

def end_remove(video, frame_number, video_extension):
    frame_raw = ""
    video_name = video[:-len(video_extension)]

    video_copy = shutil.copy2(f"{video}", f"{video_name}_original{video_extension}")
    try:
        os.remove(video)
    except PermissionError as e:
        raise RemovalError("Not enough permissions to manage your files!") from e
    probe_data = ffmpeg.probe(f"{video_copy}")
    video_stream = probe_data["streams"]

    for stream in video_stream:
        if stream["codec_type"] == "video":
            frame_raw = stream["r_frame_rate"]
            break
    numerator_str, denominator_str = frame_raw.split("/")
    frame_rate = float(numerator_str) / float(denominator_str)
    calculated_timestamp = frame_number / frame_rate

    try:
        result_of_conversion = ffmpeg.input(f"{video_copy}", ss = "0", to = f"{calculated_timestamp}").output(f"{video}", c="copy").run()
        return result_of_conversion
    except Exception as e:
        raise ConversionError(f"ffmpeg couldn't convert your video, here's why: {e}")