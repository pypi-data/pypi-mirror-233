from tetra_model_zoo.aotgan.model import AOTGAN, DEFAULT_WEIGHTS, MODEL_ID
from tetra_model_zoo.aotgan.test import IMAGE_ADDRESS, MASK_ADDRESS
from tetra_model_zoo.repaint.demo import repaint_demo


def main():
    repaint_demo(AOTGAN, MODEL_ID, DEFAULT_WEIGHTS, IMAGE_ADDRESS, MASK_ADDRESS)


if __name__ == "__main__":
    main()
