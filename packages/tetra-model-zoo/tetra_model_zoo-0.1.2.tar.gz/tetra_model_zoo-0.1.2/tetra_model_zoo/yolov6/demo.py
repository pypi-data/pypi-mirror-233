from tetra_model_zoo.yolo.demo import yolo_detection_demo
from tetra_model_zoo.yolov6.app import YoloV6DetectionApp
from tetra_model_zoo.yolov6.model import DEFAULT_WEIGHTS, MODEL_ID, YoloV6
from tetra_model_zoo.yolov6.test import IMAGE_ADDRESS

WEIGHTS_HELP_MSG = (
    "YoloV6 checkpoint name, defined here: https://github.com/meituan/YOLOv6/releases"
)


def main():
    yolo_detection_demo(
        YoloV6,
        MODEL_ID,
        DEFAULT_WEIGHTS,
        WEIGHTS_HELP_MSG,
        YoloV6DetectionApp,
        IMAGE_ADDRESS,
        YoloV6.STRIDE_MULTIPLE,
    )


if __name__ == "__main__":
    main()
