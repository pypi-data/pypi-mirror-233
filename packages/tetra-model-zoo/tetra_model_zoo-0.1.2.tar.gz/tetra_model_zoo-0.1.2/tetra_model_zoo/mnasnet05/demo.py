from tetra_model_zoo.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.mnasnet05.model import DEFAULT_WEIGHTS, MODEL_ID, MNASNet05


def main():
    imagenet_demo(MNASNet05, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
