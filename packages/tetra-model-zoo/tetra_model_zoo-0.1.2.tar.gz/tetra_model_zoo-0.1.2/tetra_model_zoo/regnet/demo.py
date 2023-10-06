from tetra_model_zoo.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.regnet.model import DEFAULT_WEIGHTS, MODEL_ID, RegNet


def main():
    imagenet_demo(RegNet, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
