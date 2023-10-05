import pytest
from motion_detector_g4 import MotionDetector
from cv2 import cv2


frame_1_path = 'tests/images/02_frame_1.png'
frame_2_path = 'tests/images/02_frame_2.png'

frame_1 = cv2.imread(frame_1_path)
frame_2 = cv2.imread(frame_2_path)


def test_1():
    md = MotionDetector()
    md.apply_first_frame(frame_1)
    assert md.check_motion(frame_2) is False
