import ffmpeg
import os
import shutil

def endRemove(video, frameNumber, videoExtension):
    videoOriginal = video
    videoName = video[:-len(videoExtension)]

    videoCopy = shutil.copy2(f"{video}", f"{videoName}_original{videoExtension}")
    try:
        os.remove(video)
    except:
        return "Error"
    probeData = ffmpeg.probe(f"{videoCopy}")
    videoStream = probeData["streams"]
    streamNum = 0

    for stream in videoStream:
        if stream["codec_type"] == "video":
            frameRaw = stream["r_frame_rate"]
            break
    numeratorStr, denominatorStr = frameRaw.split("/")
    frameRate = float(numeratorStr) / float(denominatorStr)
    calculatedTimestamp = frameNumber / frameRate

    try:
        ffmpeg.input(f"{videoCopy}", ss = "0", to = f"{calculatedTimestamp}").output(f"{video}", c="copy").run()
    except:
        return "Error"