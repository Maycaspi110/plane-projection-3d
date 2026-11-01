import cv2
import nrrd
import numpy as np
import sys
import Ex0


def run_demo(tmp_path, monkeypatch, csv_text):
    # runs the demo main like "python Ex0.py file.nrrd file.csv file.mp4"
    volume = (np.arange(20 * 20 * 20) % 200).reshape(20, 20, 20).astype(np.uint8)
    nrrd.write(str(tmp_path / "v.nrrd"), volume)
    (tmp_path / "p.csv").write_text(csv_text)
    out = tmp_path / "out.mp4"
    monkeypatch.setattr(sys, "argv", ["Ex0.py", str(tmp_path / "v.nrrd"), str(tmp_path / "p.csv"), str(out)])
    return Ex0.main(), out


def test_demo_makes_a_frame_for_every_row(tmp_path, monkeypatch):
    result, out = run_demo(tmp_path, monkeypatch, "10,2,5,2,18,5,18,18,5\n10,2,8,2,18,8,18,18,8\n")
    assert result == 0
    video = cv2.VideoCapture(str(out))
    assert int(video.get(cv2.CAP_PROP_FRAME_COUNT)) == 2
    video.release()


def test_demo_invalid_row_becomes_error_frame(tmp_path, monkeypatch, capsys):
    # the middle row is not isosceles: it gets an error frame, the other frames are still made
    result, out = run_demo(tmp_path, monkeypatch,
                           "10,2,5,2,18,5,18,18,5\n1,2,3,4,5,6,7,8,9\n10,2,8,2,18,8,18,18,8\n")
    assert result == 0
    assert "row 2" in capsys.readouterr().out
    video = cv2.VideoCapture(str(out))
    assert int(video.get(cv2.CAP_PROP_FRAME_COUNT)) == 3
    video.release()


def test_demo_wrong_arguments(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["Ex0.py"])
    assert Ex0.main() == 1
