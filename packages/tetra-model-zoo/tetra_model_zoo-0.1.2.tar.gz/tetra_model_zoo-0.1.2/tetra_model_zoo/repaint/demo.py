import argparse
from typing import Callable, Optional

import torch

from tetra_model_zoo.repaint.app import RepaintMaskApp
from tetra_model_zoo.utils.asset_loaders import load_image


#
# Run repaint app end-to-end on a sample image.
# The demo will display the predicted image in a window.
#
def repaint_demo(
    model: Callable[..., Callable[[torch.Tensor, torch.Tensor], torch.Tensor]],
    model_id: str,
    default_weights: Optional[str],
    default_image: str,
    default_mask: str,
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
    parser.add_argument(
        "--mask",
        type=str,
        default=default_mask,
        help="test mask file path or URL",
    )
    args = parser.parse_args()

    # Load image & model
    if default_weights:
        model = model.from_pretrained(args.weights)
    else:
        model = model.from_pretrained()
    image = load_image(args.image, model_id)
    mask = load_image(args.mask, model_id)
    print("Model Loaded")

    # Run app
    app = RepaintMaskApp(model)
    image.show(title="Model Input")
    app.paint_mask_on_image(image, mask)[0].show(title="Repainted (Model Output)")
