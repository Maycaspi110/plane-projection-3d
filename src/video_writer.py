import cv2
import numpy as np
from src.framing import pad_to_size, common_frame_size
from src.intensity import normalize_to_uint8

""" Converting a list of 2D images for each plane into an MP4 video.
 vmin/vmax: The minimum and maximum values ​​for the entire volume, to ensure consistent brightness."""

def error_frame(height, width, text):
    # A black frame with a white text, for a plane that is not valid.
    frame = np.zeros((height, width), dtype=np.uint8)
    for line, y_part in (("ERROR", 0.3), (text.upper(), 0.7)):
        (text_w, text_h), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        scale = min(3, 0.9 * width / text_w, 0.25 * height / text_h)   # fit the frame
        thick = 2 if scale >= 0.6 else 1                               # thick text survives the video compression
        (text_w, text_h), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, scale, thick)
        x = max(0, (width - text_w) // 2)
        y = int(height * y_part) + text_h // 2
        cv2.putText(frame, line, (x, y), cv2.FONT_HERSHEY_SIMPLEX, scale, 255, thick)
    return frame


def write_video(images, vmin, vmax, path, fps=30):
    # An item of images is a 2D array, or a text (for example "row 3") for a bad plane:
    # that one becomes an error frame and the other frames are not affected.
    if len(images) == 0:
        raise ValueError("no images to write")

    # All frames must have the same size: the biggest image decides
    arrays = [image for image in images if not isinstance(image, str)]
    height, width = common_frame_size(arrays) if arrays else (120, 360)

    # OpenCV wants width, height here, the opposite order of numpy
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"),
                             fps, (width, height), isColor=False)
    if not writer.isOpened():
        raise ValueError(str(path) + ": cannot create video file")

    for image in images:
        if isinstance(image, str):
            writer.write(error_frame(height, width, image))
            continue
        frame = pad_to_size(image, height, width) # same size for all
        frame = normalize_to_uint8(frame, vmin, vmax) # gray levels 0-255
        writer.write(frame)   # add the frame
    writer.release() 