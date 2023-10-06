from tetra_model_zoo.real_esrgan_x4plus.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    Real_ESRGAN_x4plus,
)
from tetra_model_zoo.real_esrgan_x4plus.test import IMAGE_ADDRESS
from tetra_model_zoo.super_resolution.demo import super_resolution_demo

WEIGHTS_HELP_MSG = "RealESRGAN checkpoint `.pth` name from the Real-ESRGAN repo. Can be set to any of the model names defined here: https://github.com/xinntao/Real-ESRGAN/blob/master/docs/model_zoo.md to automatically download the file instead."


#
# Run Real-ESRGAN end-to-end on a sample image.
# The demo will display a image with the predicted bounding boxes.
#
def main():
    super_resolution_demo(
        model=Real_ESRGAN_x4plus,
        model_id=MODEL_ID,
        weights_help_msg=WEIGHTS_HELP_MSG,
        default_weights=DEFAULT_WEIGHTS,
        default_image=IMAGE_ADDRESS,
    )


if __name__ == "__main__":
    main()
