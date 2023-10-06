import argparse
from typing import Callable, Tuple

import torch

from tetra_model_zoo.super_resolution.app import SuperResolutionApp
from tetra_model_zoo.utils.asset_loaders import load_image


#
# Run Super Resolution end-to-end on a sample image.
# The demo will display a image with the predicted bounding boxes.
#
def super_resolution_demo(
    model: Callable[[torch.Tensor], Tuple[torch.Tensor, torch.Tensor, torch.Tensor]],
    model_id: str,
    default_weights: str,
    weights_help_msg: str,
    default_image: str,
):
    # Demo parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--weights", type=str, default=default_weights, help=weights_help_msg
    )
    parser.add_argument(
        "--image",
        type=str,
        default=default_image,
        help="image file path or URL.",
    )

    args = parser.parse_args()

    # Load image & model
    model = model.from_pretrained(args.weights)
    app = SuperResolutionApp(model)
    print("Model Loaded")
    image = load_image(args.image, model_id)
    pred_images = app.upscale_image(image)
    image.show()
    pred_images[0].show()
