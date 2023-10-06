import cv2
from multipledispatch import dispatch
from numpy import ndarray


@dispatch(str, str)
def compare_frames(frame_path_1: str, frame_path_2: str) -> bool:
    """
    Compare 2 frames

    :param frame_path_1: Path to frame 1
    :type frame_path_1: str
    :param frame_path_2: Path to frame 2
    :type frame_path_2: str
    :return: bool
    """

    # TODO: Check different frames size

    frame_1 = cv2.imread(frame_path_1)
    frame_2 = cv2.imread(frame_path_2)

    return compare_frames(frame_1, frame_2)


@dispatch(ndarray, ndarray)
def compare_frames(frame_1: ndarray, frame_2: ndarray) -> bool:
    """
    Compare 2 frames

    :param frame_1:
    :type frame_1: numpy.ndarray
    :param frame_2: Path to frame 2
    :type frame_2: numpy.ndarray
    :return: bool
    """

    # TODO: Check different frames size

    diff = cv2.norm(frame_1, frame_2, cv2.NORM_L2)

    if diff == 0.0:
        return True

    return False


@dispatch(str, ndarray)
def compare_frames(frame_path_1: str, frame_2: ndarray) -> bool:
    """
    Compare 2 frames

    :param frame_path_1: Path to frame 1
    :type frame_path_1: str
    :param frame_2:
    :type frame_2: numpy.ndarray
    :return: bool
    """

    # TODO: Check different frames size

    frame_1 = cv2.imread(frame_path_1)

    return compare_frames(frame_1, frame_2)


@dispatch(ndarray, str)
def compare_frames(frame_1: ndarray, frame_path_2: str) -> bool:
    """
    Compare 2 frames

    :param frame_1:
    :type frame_1: numpy.ndarray
    :param frame_path_2: Path to frame 2
    :type frame_path_2: str
    :return: bool
    """

    # TODO: Check different frames size

    frame_2 = cv2.imread(frame_path_2)

    return compare_frames(frame_1, frame_2)
