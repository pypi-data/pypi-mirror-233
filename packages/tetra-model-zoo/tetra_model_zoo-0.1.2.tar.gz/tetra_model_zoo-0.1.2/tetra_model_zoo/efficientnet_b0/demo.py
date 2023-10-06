from tetra_model_zoo.efficientnet_b0.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    EfficientNetB0,
)
from tetra_model_zoo.imagenet_classifier.demo import imagenet_demo


def main():
    imagenet_demo(EfficientNetB0, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
