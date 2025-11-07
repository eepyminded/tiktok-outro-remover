import os
import endingDetecter
import endingRemover

def fileLooper(directory):
    files = []

    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            files.append(os.path.join(directory, file))
        else:
            continue

    for file in files:
        if file.endswith((".mp4", ".webm", ".mov", "mkv")):
            splitFile = os.path.splitext(file)
            videoExtension = splitFile[1]
            videoFrame = endingDetecter.endingDetect(file)

            # no ending detected
            if videoFrame == False:
                continue
            else:
                endingRemover.endRemove(file, videoFrame, videoExtension)