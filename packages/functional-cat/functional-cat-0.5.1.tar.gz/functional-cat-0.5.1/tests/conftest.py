from typing import List

import pytest
from PIL import Image

from functional_cat.data_types import (
    BoundingPolygon,
    Detection,
    DetectionWithKeypoints,
    Keypoint,
)
from functional_cat.interfaces import ObjectDetector


def compare_boundaries(
    b1: BoundingPolygon, b2: BoundingPolygon, tol: int = 7
) -> None:
    int_pts1 = [(round(pt.x), round(pt.y)) for pt in b1.points]
    int_pts2 = [(round(pt.x), round(pt.y)) for pt in b2.points]

    assert len(int_pts1) == len(int_pts2)

    for pt1 in int_pts1[:]:
        for pt2 in int_pts2[:]:
            if abs(pt1[0] - pt2[0]) <= tol and abs(pt1[1] - pt2[1]) <= tol:
                int_pts1.remove(pt1)
                int_pts2.remove(pt2)
                break

    assert int_pts1 == []
    assert int_pts2 == []


def compare_keypoints(
    kps1: List[Keypoint], kps2: List[Keypoint], tol: int = 4
):
    assert len(kps1) == len(kps2)

    def sort_fn(k):
        return k.class_label

    kps1 = sorted(kps1, key=sort_fn)
    kps2 = sorted(kps2, key=sort_fn)

    for kp1, kp2 in zip(kps1, kps2):
        assert kp1.class_label == kp2.class_label
        assert abs(kp1.x - kp2.x) <= tol
        assert abs(kp1.y - kp2.y) <= tol
        assert kp1.score == kp2.score
        assert kp1.visible == kp2.visible


def compare_detection_output(
    dets1: List[List[Detection]], dets2: List[List[Detection]]
) -> None:
    assert len(dets1) == len(dets2)

    for img_dets1, img_dets2 in zip(dets1, dets2):
        assert len(img_dets1) == len(img_dets2)
        for det1, det2 in zip(img_dets1, img_dets2):
            # order of detections might be different. so could try to
            # turn detections into a set. but then issue if bounding boxes
            # are not exactly equal. maybe can order by the score. but this
            # is working for now
            assert det1.class_label == det2.class_label
            assert abs(det1.score - det2.score) <= 0.01

            assert hasattr(det1, "keypoints") == hasattr(det2, "keypoints")
            if hasattr(det1, "keypoints"):
                compare_keypoints(det1.keypoints, det2.keypoints)

            compare_boundaries(det1.boundary, det2.boundary)


def compare_detection_with_keypoints_output(
    dets1: List[List[DetectionWithKeypoints]],
    dets2: List[List[DetectionWithKeypoints]],
) -> None:
    compare_detection_output(dets1, dets2)


@pytest.fixture
def check_detection_batch_processing():
    def fn(
        model: ObjectDetector,
        img1: Image.Image,
        img2: Image.Image,
        score_thres: float,
    ):
        out1 = model([img1], score_thres=score_thres)
        out2 = model([img2], score_thres=score_thres)

        batched_out = model([img1, img2], score_thres=score_thres)

        compare_detection_output(out1 + out2, batched_out)
        return batched_out

    return fn
