import pytest
from compare_frames_g4 import compare_frames
from cv2 import cv2


frame_1_path = 'tests/frames_compareFrames/frame_1.png'
frame_1_good_path = 'tests/frames_compareFrames/frame_1_good.png'
frame_1_bad_path = 'tests/frames_compareFrames/frame_1_bad.png'

frame_1 = cv2.imread(frame_1_path)
frame_1_good = cv2.imread(frame_1_good_path)
frame_1_bad = cv2.imread(frame_1_bad_path)


def test_1():
    assert compare_frames(frame_1_path,
                          frame_1_good_path
                          ) is True

    assert compare_frames(frame_1_path,
                          frame_1_bad_path
                          ) is False


def test_2():
    assert compare_frames(frame_1,
                          frame_1_good
                          ) is True

    assert compare_frames(frame_1,
                          frame_1_bad
                          ) is False


def test_3():
    assert compare_frames(frame_1,
                          frame_1_good_path
                          ) is True

    assert compare_frames(frame_1_path,
                          frame_1_good
                          ) is True

    assert compare_frames(frame_1,
                          frame_1_bad_path
                          ) is False

    assert compare_frames(frame_1_path,
                          frame_1_bad
                          ) is False
