from tetra_model_zoo.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.mobilenet_v3_small.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    MobileNetV3Small,
)


def main():
    imagenet_demo(MobileNetV3Small, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
