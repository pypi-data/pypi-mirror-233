import argparse
from typing import Callable, Optional

import torch
from PIL.Image import fromarray

from tetra_model_zoo.unet_segmentation.app import UNetSegmentationApp
from tetra_model_zoo.unet_segmentation.model import DEFAULT_WEIGHTS, MODEL_ID, UNet
from tetra_model_zoo.unet_segmentation.test import IMAGE_ADDRESS
from tetra_model_zoo.utils.asset_loaders import load_image


#
# Run unet segmentation app end-to-end on a sample image.
# The demo will display the predicted mask in a window.
#
def unet_demo(
    model: Callable[..., Callable[[torch.Tensor, torch.Tensor], torch.Tensor]],
    model_id: str,
    default_weights: Optional[str],
    default_image: str,
):
    # Demo parameters
    parser = argparse.ArgumentParser()
    if default_weights:
        parser.add_argument(
            "--weights", type=str, default=default_weights, help="Model weights"
        )
    parser.add_argument(
        "--image",
        type=str,
        default=default_image,
        help="test image file path or URL",
    )
    args = parser.parse_args()

    # Load image & model
    if default_weights:
        model = model.from_pretrained(args.weights)
    else:
        model = model.from_pretrained()
    image = load_image(args.image, model_id)
    print("Model Loaded")

    # Run app
    app = UNetSegmentationApp(model)
    image.show(title="Model Input")
    mask = fromarray(app.predict(image))
    mask.show(title="Mask (Model Output)")


def main():
    unet_demo(
        UNet,
        MODEL_ID,
        DEFAULT_WEIGHTS,
        IMAGE_ADDRESS,
    )


if __name__ == "__main__":
    main()
