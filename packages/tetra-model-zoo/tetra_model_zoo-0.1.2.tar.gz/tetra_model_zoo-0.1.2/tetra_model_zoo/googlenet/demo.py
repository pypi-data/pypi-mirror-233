from tetra_model_zoo.googlenet.model import DEFAULT_WEIGHTS, MODEL_ID, GoogLeNet
from tetra_model_zoo.imagenet_classifier.demo import imagenet_demo


def main():
    imagenet_demo(GoogLeNet, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
