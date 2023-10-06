import pytest
import cv2
from polyfiller_g4 import PolyFiller
from compare_frames_g4 import compare_frames
from numpy import ndarray


frame_1_path = 'tests/images/frame_1.png'
frame_1 = cv2.imread(frame_1_path)

frame_2_path = 'tests/images/frame_2.png'
frame_2 = cv2.imread(frame_2_path)


def test_1():

    pf = PolyFiller()

    frame_fill = pf.fill(frame_1)

    assert compare_frames(frame_1, frame_fill) is True


def test_2():

    pf = PolyFiller()
    pf.add_polygon([[750, 500], [850, 500], [800, 600]])
    pf.add_polygon([[1000, 600], [1100, 650], [1200, 800], [900, 650]])
    frame_fill = pf.fill(frame_1)

    (b, g, r) = frame_fill[530, 800]
    assert int(r) + int(g) + int(b) == 0

    (b, g, r) = frame_fill[640, 970]
    assert int(r) + int(g) + int(b) == 0

    (b, g, r) = frame_fill[730, 1123]
    assert int(r) + int(g) + int(b) == 0

    (b, g, r) = frame_fill[551, 771]
    assert int(r) + int(g) + int(b) == 309

    (b, g, r) = frame_fill[564, 824]
    assert int(r) + int(g) + int(b) == 321

    (b, g, r) = frame_fill[711, 1007]
    assert int(r) + int(g) + int(b) == 456

    (b, g, r) = frame_fill[672, 1123]
    assert int(r) + int(g) + int(b) == 477


def test_3():

    pf = PolyFiller(color=(100, 250, 50))
    pf.add_polygon([[750, 500], [850, 500], [800, 600]])
    pf.add_polygon([[1000, 600], [1100, 650], [1200, 800], [900, 650]])
    frame_fill = pf.fill(frame_1)

    (b, g, r) = frame_fill[530, 800]
    assert int(r) + int(g) + int(b) == 400

    (b, g, r) = frame_fill[640, 970]
    assert int(r) + int(g) + int(b) == 400

    (b, g, r) = frame_fill[730, 1123]
    assert int(r) + int(g) + int(b) == 400

    (b, g, r) = frame_fill[551, 771]
    assert int(r) + int(g) + int(b) == 309

    (b, g, r) = frame_fill[564, 824]
    assert int(r) + int(g) + int(b) == 321

    (b, g, r) = frame_fill[711, 1007]
    assert int(r) + int(g) + int(b) == 456

    (b, g, r) = frame_fill[672, 1123]
    assert int(r) + int(g) + int(b) == 477


def test_4():

    pf = PolyFiller(color=(100, 250, 50))
    pf.add_polygon([[750, 500], [850, 500], [800, 600]])
    pf.add_polygon([[1000, 600], [1100, 650], [1200, 800], [900, 650]])
    pf.fill(frame_1)
    frame_fill = pf.fill(frame_2)

    (b, g, r) = frame_fill[530, 800]
    assert int(r) + int(g) + int(b) == 400

    (b, g, r) = frame_fill[640, 970]
    assert int(r) + int(g) + int(b) == 400

    (b, g, r) = frame_fill[730, 1123]
    assert int(r) + int(g) + int(b) == 400

    (b, g, r) = frame_fill[551, 771]
    assert int(r) + int(g) + int(b) == 318

    (b, g, r) = frame_fill[564, 824]
    assert int(r) + int(g) + int(b) == 315

    (b, g, r) = frame_fill[711, 1007]
    assert int(r) + int(g) + int(b) == 438

    (b, g, r) = frame_fill[672, 1123]
    assert int(r) + int(g) + int(b) == 483
