from tetra_model_zoo.convnext_tiny.model import DEFAULT_WEIGHTS, MODEL_ID, ConvNextTiny
from tetra_model_zoo.imagenet_classifier.demo import imagenet_demo


def main():
    imagenet_demo(ConvNextTiny, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
