import argparse

from tetra_model_zoo.litehrnet.app import LiteHRNetApp
from tetra_model_zoo.litehrnet.model import DEFAULT_INFERENCER_ARCH, MODEL_ID, LiteHRNet
from tetra_model_zoo.litehrnet.test import IMAGE_ADDRESS
from tetra_model_zoo.utils.asset_loaders import load_image

IA_HELP_MSG = "More inferencer architectures for litehrnet can be found at https://github.com/open-mmlab/mmpose/tree/main/configs/body_2d_keypoint/topdown_heatmap/coco"


#
# Run LiteHRNet end-to-end on a sample image.
# The demo will display a image with the predicted keypoints.
#
def main():
    # Demo parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inferencer_arch", type=str, default=DEFAULT_INFERENCER_ARCH, help=IA_HELP_MSG
    )
    parser.add_argument(
        "--image",
        type=str,
        default=IMAGE_ADDRESS,
        help="image file path or URL",
    )

    args = parser.parse_args()

    # Load image & model
    model = LiteHRNet.from_pretrained(args.inferencer_arch)
    image = load_image(args.image, MODEL_ID)
    print("Model Loaded")

    app = LiteHRNetApp(model, model.inferencer)
    app.predict_pose_keypoints(image)[0].show()


if __name__ == "__main__":
    main()
