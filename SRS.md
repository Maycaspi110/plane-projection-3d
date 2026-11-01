# plane-projection-3d: Software Requirements Specification (SRS)

## 1. Introduction
The program gets a 3D scan (an NRRD file) and a list of planes (a CSV file), and makes a video. Every frame in the video is a 2D cut of the scan along one plane.

It is a command-line program, with no graphical interface. It is meant for doctors, researchers and people who build medical imaging software.

```bash
python Ex0.py <volume.nrrd> <planes.csv> <output.mp4>
```

### 1.1 Scope
- **In scope:** reading an NRRD volume and a CSV of planes, computing the 2D image of each plane, and writing the images to an MP4 video.
- **Out of scope:** a graphical interface, a 3D viewer, and editing or saving the volume.

### 1.2 Definitions
| Term | Meaning |
|------|---------|
| Voxel | One cell of the 3D matrix, M[x][y][z] |
| NRRD | A file format that stores a 3D scan (for example an MRI) |
| Plane | A flat surface in 3D, given by an isosceles triangle (3 points) or an isosceles trapezoid (4 points) |
| Frame | One 2D image in the video, made from one plane |
| FPS | Frames per second |

### 1.3 Assumptions and Constraints
- The program is written in Python. It uses NumPy for the computation and OpenCV for the video.
- The whole volume fits in memory (a 500x500x500 byte volume is about 125 MB).
- The coordinates in the CSV are in voxel units, in the order x,y,z (the axes of the matrix M).

## 2. Inputs and Outputs
**Inputs**
- **Volume (.nrrd):** a 3D matrix of size sx x sy x sz (each side from 1 up to 2^10 - 1). Each value is an unsigned integer of 8, 16 or 32 bits.
- **Planes (.csv):** each row is one plane, given by 3 or 4 points, with x,y,z for each point.
  - 9 numbers = isosceles triangle.
  - 12 numbers = isosceles trapezoid.
  - A header line, and a first column with the number of points (3 or 4), are also accepted.

**Output**
- **Video (.mp4):** one frame per CSV row, in the same order as the rows. It is grayscale, at 30 FPS. All frames have the same size: the biggest width and the biggest height among all the planes.
- **Frame size:** the projection makes an image at natural scale (1 pixel = 1 voxel unit). Then the image is padded with black (0), in the center, up to the frame size. It is never resized, so every pixel is a real value from the scan.

## 3. Functional Requirements
- **FR1:** The program reads the volume from the NRRD file and the planes from the CSV file.
- **FR2:** For each plane, the program samples the volume along the plane and makes a 2D image. A point outside the volume gets the value 0.
- **FR3:** Each sample takes the value of the nearest voxel (no interpolation).
- **FR4:** The program scales the values to 0-255, using the minimum and the maximum of the whole volume (computed once), so the brightness is the same in all frames. The results are clipped to 0-255, so a point outside the volume (value 0), even if it is below the volume minimum, stays black.
- **FR5:** The program pads each image with black (0), in the center, up to the frame size, without resizing it.
- **FR6:** The program writes all the images, in order, to the MP4 file.

## 4. Non-Functional Requirements
- **NFR1 (Performance):** for a 500x500x500 volume, at least 30 frames per second (the target is 100).
- **NFR2 (Efficiency):** the computation is vectorized (NumPy) and does not loop over single pixels, so it can reach NFR1.
- **NFR3 (Stability):** the program does not crash on valid input, and prints a clear error message on invalid input (an error frame for a bad plane row).

## 5. Edge Cases and Error Handling
A bad row in the CSV does not stop the video. The program prints the row number and the reason, puts an "error frame" in the video for that row (a black frame with the text ERROR and the row number), and goes on with the other rows. So the video still has one frame per CSV row, in the same order, and the valid rows get their correct frames. This is what the lecturer asked for in the Q&A. The code that reads the CSV raises an exception for an invalid row (`read_planes`), and the demo handles it row by row.

**Bad rows (error frame, the program continues):**
- A CSV row has a wrong number of values (not 9 or 12), or a value that is not a number.
- A CSV row has two identical points (the plane is degenerate).
- The plane is not isosceles: in a triangle `|dist(a,b) - dist(a,c)| >= 0.001`, and in a trapezoid the two legs differ by 0.001 or more.
- In a trapezoid, `dist(a1,a2) > dist(b,c)`.
- The 4 points of a trapezoid are not on one plane.

**Errors (print a message and stop):**
- The command line does not have exactly 3 arguments (the usage line is printed).
- A file is missing, cannot be read, or is empty.
- The NRRD file is not a 3D volume of unsigned integers.
- The output file cannot be written.

**Not errors:**
- A plane that is partly or fully outside the volume: the points outside get 0 (black).
- Coordinates that are not whole numbers (for example 12.5): rounded to the nearest voxel.
- All voxels have the same value (min = max): all frames are black, so there is no division by zero.
- A volume with a side of size 1: handled like any other volume.
