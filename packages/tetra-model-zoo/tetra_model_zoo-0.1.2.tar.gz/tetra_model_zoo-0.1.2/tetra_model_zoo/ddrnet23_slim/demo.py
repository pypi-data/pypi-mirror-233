import argparse

from tetra_model_zoo.ddrnet23_slim.app import DDRNetApp
from tetra_model_zoo.ddrnet23_slim.model import MODEL_ID, DDRNet
from tetra_model_zoo.ddrnet23_slim.test import INPUT_IMAGE_ADDRESS
from tetra_model_zoo.utils.asset_loaders import load_image


#
# Run DDRNet end-to-end on a sample image.
# The demo will display a image with the predicted segmentation map overlaid.
#
def main():
    # Demo parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--weights",
        type=str,
        default=None,
        help="DDRNet checkpoint `.pt` path on disk.",
    )
    parser.add_argument(
        "--image",
        type=str,
        default=INPUT_IMAGE_ADDRESS,
        help="image file path or URL",
    )
    args = parser.parse_args()

    # Load image & model
    model = DDRNet.from_pretrained(args.weights)
    image = load_image(args.image, MODEL_ID)
    print("Model Loaded")

    app = DDRNetApp(model)
    app.segment_image(image)[0].show()


if __name__ == "__main__":
    main()
