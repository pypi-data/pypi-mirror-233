from tetra_model_zoo.yolo.demo import yolo_detection_demo
from tetra_model_zoo.yolov8_det.app import YoloV8DetectionApp
from tetra_model_zoo.yolov8_det.model import DEFAULT_WEIGHTS, MODEL_ID, YoloV8Detector
from tetra_model_zoo.yolov8_det.test import IMAGE_ADDRESS

WEIGHTS_HELP_MSG = f"YoloV8 checkpoint name. Valid checkpoints can be found in tetra_model_zoo/{MODEL_ID}/model.py"


def main():
    yolo_detection_demo(
        YoloV8Detector,
        MODEL_ID,
        DEFAULT_WEIGHTS,
        WEIGHTS_HELP_MSG,
        YoloV8DetectionApp,
        IMAGE_ADDRESS,
    )


if __name__ == "__main__":
    main()
