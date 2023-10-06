from tetra_model_zoo.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.mobilenet_v2.model import DEFAULT_WEIGHTS, MODEL_ID, MobileNetV2


def main():
    imagenet_demo(MobileNetV2, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
