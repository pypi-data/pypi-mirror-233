from tetra_model_zoo.lama_dilated.model import DEFAULT_WEIGHTS, MODEL_ID, LamaDilated
from tetra_model_zoo.lama_dilated.test import IMAGE_ADDRESS, MASK_ADDRESS
from tetra_model_zoo.repaint.demo import repaint_demo


def main():
    repaint_demo(LamaDilated, MODEL_ID, DEFAULT_WEIGHTS, IMAGE_ADDRESS, MASK_ADDRESS)


if __name__ == "__main__":
    main()
