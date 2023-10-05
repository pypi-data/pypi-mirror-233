import pytest
from motion_detector_g4 import MotionDetector
from cv2 import cv2


frame_1_path = 'tests/images/03_frame_1.bmp'
frame_2_path = 'tests/images/03_frame_2.bmp'
frame_3_path = 'tests/images/03_frame_3.bmp'
frame_4_path = 'tests/images/03_frame_4.bmp'


def test_1():
    md = MotionDetector()
    md.apply_first_frame(frame_1_path)
    assert md.check_motion(frame_2_path) is False


def test_2():
    md = MotionDetector()
    md.apply_first_frame(frame_1_path)
    assert md.check_motion(frame_2_path) is False
    assert md.check_motion(frame_3_path) is False


def test_3():
    md = MotionDetector()
    md.apply_first_frame(frame_3_path)
    assert md.check_motion(frame_4_path) is True
