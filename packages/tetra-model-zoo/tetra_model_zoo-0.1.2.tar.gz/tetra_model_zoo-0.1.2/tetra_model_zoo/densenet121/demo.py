from tetra_model_zoo.densenet121.model import DEFAULT_WEIGHTS, MODEL_ID, DenseNet
from tetra_model_zoo.imagenet_classifier.demo import imagenet_demo


def main():
    imagenet_demo(DenseNet, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
