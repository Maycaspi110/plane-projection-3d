"""# Ex0.py - the demo. Reads a 3D scan (NRRD) and a list of planes (CSV),
# builds one 2D image per plane, and writes all images to an MP4 video.
# Usage: python Ex0.py <volume.nrrd> <planes.csv> <output.mp4>"""

import sys
from src.volume_loader import load_volume
from src.plane_input import read_rows
from src.slicer import project_plane_fast
from src.video_writer import write_video


def split_plane(numbers):
    # Turn a flat list of 9 or 12 numbers into points: start1, start2, b, c.
    points = [numbers[i:i + 3] for i in range(0, len(numbers), 3)]
    if len(points) == 3:            # triangle: a, b, c
        a, b, c = points
        return a, a, b, c           # both runners start at a
    a1, b, a2, c = points           # trapezoid: a', b, a'', c
    return a1, a2, b, c


def main():
    if len(sys.argv) != 4:
        print("usage: python Ex0.py <volume.nrrd> <planes.csv> <output.mp4>")
        return 1
    nrrd_path, csv_path, mp4_path = sys.argv[1:4]
    try:
        volume = load_volume(nrrd_path)
        vmin, vmax = volume.min(), volume.max()   # computed once for all frames
        rows = read_rows(csv_path)
        images = []
        bad = 0
        for line_number, numbers, error in rows:
            if error is not None:
                # not a valid plane: print why, and put an error frame in the video
                print("Invalid plane, row " + str(line_number) + ": " + error)
                images.append("row " + str(line_number))
                bad += 1
                continue
            start1, start2, b, c = split_plane(numbers)
            images.append(project_plane_fast(volume, start1, start2, b, c))
        write_video(images, vmin, vmax, mp4_path)
    except ValueError as error:
        print("Error:", error)
        return 1
    print("Done:", len(images), "frames written to", mp4_path)
    if bad:
        print(str(bad) + " invalid plane(s) became error frames")
    return 0


if __name__ == "__main__":
    sys.exit(main())