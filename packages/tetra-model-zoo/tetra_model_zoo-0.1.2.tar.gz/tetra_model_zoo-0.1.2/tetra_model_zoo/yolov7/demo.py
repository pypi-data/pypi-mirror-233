from tetra_model_zoo.yolo.demo import yolo_detection_demo
from tetra_model_zoo.yolov7.app import YoloV7DetectionApp
from tetra_model_zoo.yolov7.model import DEFAULT_WEIGHTS, MODEL_ID, YoloV7
from tetra_model_zoo.yolov7.test import IMAGE_ADDRESS

WEIGHTS_HELP_MSG = "YoloV7 checkpoint `.pt` path on disk. Can be set to any of the strings defined here: https://github.com/WongKinYiu/yolov7/blob/main/utils/google_utils.py#L29 to automatically download the file instead."


def main():
    yolo_detection_demo(
        YoloV7,
        MODEL_ID,
        DEFAULT_WEIGHTS,
        WEIGHTS_HELP_MSG,
        YoloV7DetectionApp,
        IMAGE_ADDRESS,
        YoloV7.STRIDE_MULTIPLE,
    )


if __name__ == "__main__":
    main()
