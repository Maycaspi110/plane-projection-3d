import numpy as np

EPS = 0.001   # tolerance given by the lecturer (Q&A of the assignment)

def plane_kind(numbers):

      # Decide the plane shape by counting the numbers in a CSV row:
    # 9 numbers = 3 points = triangle, 12 numbers = 4 points = trapezoid.

    if len(numbers) == 9:
        return "triangle"
    if len(numbers) == 12:
        return "trapezoid"

     # Edge case E3: wrong amount of numbers
    raise ValueError("a plane row must have 9 or 12 numbers, got " + str(len(numbers)))


def check_shape(numbers):
    # Edge cases E5, E10: the points must really form an isosceles triangle
    # or an isosceles trapezoid (rules and EPS from the assignment Q&A).
    pts = np.array(numbers, dtype=np.float64).reshape(-1, 3)
    dist = lambda p, q: float(np.linalg.norm(p - q))
    if plane_kind(numbers) == "triangle":
        a, b, c = pts
        if abs(dist(a, b) - dist(a, c)) >= EPS:
            raise ValueError("triangle is not isosceles: dist(a,b) != dist(a,c)")
        return
    a1, b, a2, c = pts               # same order as in the CSV: a', b, a'', c
    if abs(dist(a1, b) - dist(a2, c)) >= EPS:
        raise ValueError("trapezoid legs have different lengths")
    if dist(a1, a2) > dist(b, c) + EPS:
        raise ValueError("trapezoid: dist(a',a'') must not be larger than dist(b,c)")
    # the 4 points must lie on one plane: c must be within EPS of the plane of a', b, a''
    n = np.cross(b - a1, a2 - a1)
    if np.linalg.norm(n) < 1e-9:     # a' = a'': the plane is given by a', b, c
        n = np.cross(b - a1, c - a1)
    if np.linalg.norm(n) < 1e-9:
        raise ValueError("the points are on one line, they do not define a plane")
    if abs(np.dot(n, c - a1)) / np.linalg.norm(n) > EPS:
        raise ValueError("the 4 points are not on the same plane")


def read_planes(path):
    # Read the CSV file and return a list of planes (each a list of numbers).
    # The first bad row raises ValueError with the row number (the lecturer asked
    # for an exception on an invalid set of points).
    planes = []
    for line_number, numbers, error in read_rows(path):
        if error is not None:
            raise ValueError("row " + str(line_number) + ": " + error)
        planes.append(numbers)
    return planes


def read_rows(path):
    # Read the CSV file and return one entry per plane row: (row number, numbers, error).
    # For a good row error is None, for a bad row numbers is None and error says why.
    # The demo uses this to put an "error frame" in the video for a bad row.
    # Two layouts are accepted: plain rows of 9 or 12 numbers, or rows that start
    # with the number of points (3 or 4), with an optional header line first.

    try:
        with open(path) as f:
            lines = f.readlines()
    except OSError:  # Edge case E1: file missing or unreadable
        raise ValueError(str(path) + ": cannot read CSV file") from None

     # enumerate numbers the lines from 1, so errors can name the row
    rows = []
    for line_number, line in enumerate(lines, start=1):
        line = line.strip()
        if line == "":
            continue
        cells = [cell.strip() for cell in line.split(",")]
        while cells and cells[-1] == "":     # a triangle may have empty x4,y4,z4
            cells.pop()

        # header line (first line only): its first cell is text, e.g. "Number of Points"
        if line_number == 1 and not rows and cells and not _is_number(cells[0]):
            continue

        # Edge case E4: something that is not a number
        try:
            numbers = [float(x) for x in cells]
        except ValueError:
            rows.append((line_number, None, "contains a non-numeric value"))
            continue

        # a leading 3 or 4 that tells how many points follow: 1 + 9 or 1 + 12 numbers
        if len(numbers) in (10, 13) and numbers[0] == (len(numbers) - 1) / 3:
            numbers = numbers[1:]
        try:
            check_shape(numbers)
        except ValueError as error:
            rows.append((line_number, None, str(error)))
            continue
        rows.append((line_number, numbers, None))
    return rows


def _is_number(text):
    try:
        float(text)
        return True
    except ValueError:
        return False
