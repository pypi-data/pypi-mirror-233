from tetra_model_zoo.imagenet_classifier.demo import imagenet_demo
from tetra_model_zoo.squeezenet1_1.model import DEFAULT_WEIGHTS, MODEL_ID, SqueezeNet


def main():
    imagenet_demo(SqueezeNet, DEFAULT_WEIGHTS, MODEL_ID)


if __name__ == "__main__":
    main()
