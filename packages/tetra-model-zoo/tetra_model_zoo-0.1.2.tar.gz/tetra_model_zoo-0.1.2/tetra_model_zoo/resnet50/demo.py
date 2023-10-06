from tetra_model_zoo.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.resnet50.model import DEFAULT_WEIGHTS, MODEL_ID, ResNet50


def main():
    imagenet_demo(ResNet50, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
