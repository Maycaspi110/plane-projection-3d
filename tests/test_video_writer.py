import cv2
import numpy as np
from src.video_writer import write_video

"""The test includes three images of different sizes: (40,60), (80,50), and (30,30).
(Tiny frames such as 4x6 pixels make the mp4v codec crash from time to time, so the test uses bigger ones.)
We define a video file path in a temporary directory, `tmp_path`.
We then open the video file using `cv2.VideoCapture` and retrieve its properties.
Verification:
3 frames—one frame for each image. The common dimensions are determined by the maximum width 60 and the maximum height 80."""
def test_video_has_one_frame_per_image(tmp_path):
    images = [np.ones((40, 60)), np.ones((80, 50)), np.ones((30, 30))]
    out = tmp_path / "out.mp4"
    write_video(images, 0, 1, out)
    video = cv2.VideoCapture(str(out))
    assert int(video.get(cv2.CAP_PROP_FRAME_COUNT)) == 3
    # every frame has the common size: width 60, height 80
    assert int(video.get(cv2.CAP_PROP_FRAME_WIDTH)) == 60
    assert int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)) == 80
    video.release()


def test_text_item_becomes_error_frame(tmp_path):
    # a text instead of an image = a bad plane: it still gets a frame, same size as the others
    images = [np.ones((40, 60)), "row 2", np.ones((40, 60))]
    out = tmp_path / "out.mp4"
    write_video(images, 0, 1, out)
    video = cv2.VideoCapture(str(out))
    assert int(video.get(cv2.CAP_PROP_FRAME_COUNT)) == 3
    assert int(video.get(cv2.CAP_PROP_FRAME_WIDTH)) == 60
    assert int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)) == 40
    video.release()