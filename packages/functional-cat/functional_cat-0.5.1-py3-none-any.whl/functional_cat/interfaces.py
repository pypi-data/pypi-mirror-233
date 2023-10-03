from abc import ABC, abstractmethod
from enum import Enum
from typing import List

import numpy as np
from PIL import Image
from tqdm import tqdm

from functional_cat.data_types import (
    Detection,
    DetectionWithKeypoints,
    ImageInput,
    InstanceSegmentation,
)

__all__ = ["ObjectDetector", "InstanceSegmentationModel", "KeyPointDetector"]

# https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
detection_colors = [
    (230, 25, 75),
    (60, 180, 75),
    (255, 225, 25),
    (0, 130, 200),
    (245, 130, 48),
    (145, 30, 180),
    (70, 240, 240),
    (240, 50, 230),
    (210, 245, 60),
    (250, 190, 190),
    (0, 128, 128),
    (230, 190, 255),
    (170, 110, 40),
    (255, 250, 200),
    (128, 0, 0),
    (170, 255, 195),
    (128, 128, 0),
    (255, 215, 180),
    (0, 0, 128),
    (128, 128, 128),
]

# colors for keypoints
keypoint_colors = [
    "#e6194b",
    "#3cb44b",
    "#ffe119",
    "#4363d8",
    "#f58231",
    "#911eb4",
    "#46f0f0",
    "#f032e6",
    "#bcf60c",
    "#fabebe",
    "#008080",
    "#e6beff",
    "#9a6324",
    "#fffac8",
    "#800000",
    "#aaffc3",
    "#808000",
    "#ffd8b1",
    "#000075",
    "#808080",
    "#ffffff",
    "#000000",
]


class Task(Enum):
    OBJECT_DETECTION = "Object Detection"
    INSTANCE_SEGMENTATION = "Instance Segmentation"
    KEYPOINT_DETECTION = "KeyPoint Detection"


class ObjectDetector(ABC):
    """Base class for object detectors. These objects are all callable and take in
    a list of `PIL.Image` objects and output a list of bounding box detections.
    """

    task = Task.OBJECT_DETECTION

    @property
    @abstractmethod
    def class_labels(self) -> List[str]:
        pass

    @abstractmethod
    def __call__(
        self, imgs: ImageInput, score_thres: float
    ) -> List[List[Detection]]:
        pass

    @staticmethod
    def draw_output_on_img(
        img: Image.Image, dets: List[Detection], **kwargs
    ) -> Image.Image:
        unique_classes = set([det.class_label for det in dets])
        color_map = {
            c: detection_colors[i] for i, c in enumerate(unique_classes)
        }
        for i, det in enumerate(dets):
            img = det.draw_on_image(
                img, inplace=i != 0, color=color_map[det.class_label], **kwargs
            )
        return img


class InstanceSegmentationModel(ObjectDetector):
    task = Task.INSTANCE_SEGMENTATION

    @abstractmethod
    def __call__(self, imgs: ImageInput) -> List[List[InstanceSegmentation]]:
        pass

    @staticmethod
    def draw_output_on_img(
        img: Image.Image, dets: List[InstanceSegmentation]
    ) -> Image.Image:
        unique_classes = set([det.class_label for det in dets])
        color_map = {
            c: detection_colors[i] for i, c in enumerate(unique_classes)
        }

        for i, det in enumerate(dets):
            img = det.draw_on_image(
                img,
                inplace=i != 0,
                draw_mask=True,
                draw_bbox=False,
                color=color_map[det.class_label],
            )
        for i, det in enumerate(dets):
            img = det.draw_on_image(
                img,
                inplace=i != 0,
                draw_mask=False,
                draw_bbox=True,
                color=color_map[det.class_label],
            )

        return img


class KeyPointDetector(ObjectDetector):
    task = Task.KEYPOINT_DETECTION

    @abstractmethod
    def __call__(self, imgs: ImageInput) -> List[List[DetectionWithKeypoints]]:
        pass

    @property
    @abstractmethod
    def key_point_labels(self) -> List[str]:
        pass

    def draw_output_on_img(
        self, img: Image.Image, dets: List[DetectionWithKeypoints]
    ) -> Image.Image:
        color_map = {
            k: keypoint_colors[i] for i, k in enumerate(self.key_point_labels)
        }
        return super().draw_output_on_img(img, dets, color_map=color_map)

def run_model_on_video(video_path: str, out_path: str, model, call_kwargs: dict = None)-> None:
    call_kwargs = call_kwargs or {}
    try:
        import cv2
    except ModuleNotFoundError:
        raise ModuleNotFoundError("cv2 needs to be installed to use `run_model_on_video`.")
    
    vid = cv2.VideoCapture(video_path)
    bar = tqdm(total=vid.get(cv2.CAP_PROP_FRAME_COUNT))
    i = 0
    height, width = None, None
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = None
    while True:
        i += 1
        suc, frame = vid.read()
        if not suc:
            bar.close()
            break

        img = Image.fromarray(frame[:, :, ::-1])
        preds = model(img, **call_kwargs)
        for pred in preds:
            pred.draw_on_image(img)

        if out is None:
            height, width = img.height, img.width
            out = cv2.VideoWriter(
                out_path, fourcc, vid.get(cv2.CAP_PROP_FPS), (width, height)
            )

        out.write(np.array(img)[:, :, ::-1])
        bar.update()

    if out is not None:
        out.release()
