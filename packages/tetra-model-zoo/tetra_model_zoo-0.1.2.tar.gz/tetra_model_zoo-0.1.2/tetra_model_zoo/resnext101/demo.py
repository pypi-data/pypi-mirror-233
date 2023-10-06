from tetra_model_zoo.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.resnext101.model import DEFAULT_WEIGHTS, MODEL_ID, ResNeXt101


def main():
    imagenet_demo(ResNeXt101, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
