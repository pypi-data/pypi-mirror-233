import argparse
from typing import Callable, Optional

import torch
from PIL.Image import fromarray

from tetra_model_zoo.mediapipe_selfie.app import SelfieSegmentationApp
from tetra_model_zoo.mediapipe_selfie.model import (
    DEFAULT_WEIGHTS,
    MODEL_ID,
    SelfieSegmentation,
)
from tetra_model_zoo.mediapipe_selfie.test import IMAGE_ADDRESS
from tetra_model_zoo.utils.asset_loaders import load_image


#
# Run unet segmentation app end-to-end on a sample image.
# The demo will display the predicted mask in a window.
#
def mediapipe_selfie_demo(
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
    app = SelfieSegmentationApp(model)
    image.show(title="Model Input")
    mask = app.predict(image) * 255.0
    mask = fromarray(mask).convert("L")
    mask.show(title="Mask (Model Output)")


def main():
    mediapipe_selfie_demo(
        SelfieSegmentation,
        MODEL_ID,
        DEFAULT_WEIGHTS,
        IMAGE_ADDRESS,
    )


if __name__ == "__main__":
    main()
