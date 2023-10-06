from tetra_model_zoo.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.resnext50.model import DEFAULT_WEIGHTS, MODEL_ID, ResNeXt50


def main():
    imagenet_demo(ResNeXt50, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
