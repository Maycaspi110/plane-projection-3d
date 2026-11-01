# Testing Strategy

## 1. Goals
Verify that the system is correct, stable, and fast enough (at least 30 fps
on a 500x500x500 volume), using the data set defined in DATASET.md.

## 2. Level 1: Unit Tests
Each small function is tested alone with known input and expected output.

| ID | Function | Input | Expected result |
|----|----------|-------|-----------------|
| U1 | normalize | value 250, min 0, max 1000 | 64 |
| U2 | normalize | min = max | 0, no crash |
| U3 | parse CSV row | 9 values | triangle |
| U4 | parse CSV row | 12 values | trapezoid |
| U5 | parse CSV row | 10 values | error with row number |
| U6 | isosceles check | legs of different length | rejected |
| U7 | sample voxel | point outside the volume | 0 |

## 3. Level 2: Algorithm Tests
The projection is run on synthetic volumes where the correct result is known.

| ID | Data set | Plane | Expected result |
|----|----------|-------|-----------------|
| A1 | D2 (tree trunk) | cross-section | concentric circles, centered |
| A2 | D2 (tree trunk) | lengthwise | vertical stripes |
| A3 | D2 | plane fully outside the volume | all-black image |
| A4 | D2 | trapezoid plane | same result as a triangle covering the same area |

## 4. Level 3: Demo Test (end to end)
Run the demo exactly as a user would:

    python Ex0.py data-NRRD/tree_trunk.nrrd data-CSV/trunk_rotate.csv output.mp4

| ID | Check | Expected result |
|----|-------|-----------------|
| E1 | output.mp4 exists | yes |
| E2 | number of frames | equals the number of CSV rows |
| E3 | frame size | all frames have the same size: the largest width and height among all planes |
| E4 | CSV with an invalid row | message with the row number, that row becomes an error frame, the other frames are correct (`tests/test_demo.py`) |
| E5 | missing input file | clear error message |
| E6 | run on D1 (MRI) | video opens, anatomy is visible (visual check) |

## 5. Performance Test
Run `python -m scripts.benchmark` (500x500x500 volume) and read the frames per second.
Pass: at least 30 fps. Target: 100 fps.

## 6. How to Run
Tests are written with pytest: `pytest tests/`