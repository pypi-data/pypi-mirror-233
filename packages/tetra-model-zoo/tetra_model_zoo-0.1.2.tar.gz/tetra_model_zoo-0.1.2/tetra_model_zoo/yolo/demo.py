from __future__ import annotations

import argparse
from typing import Callable, Tuple

import torch
from PIL import Image

from tetra_model_zoo.utils.asset_loaders import load_image
from tetra_model_zoo.yolo.app import YoloObjectDetectionApp


#
# Run Yolo end-to-end on a sample image.
# The demo will display a image with the predicted bounding boxes.
#
def yolo_detection_demo(
    model_type: Callable[
        ..., Callable[[torch.Tensor], Tuple[torch.Tensor, torch.Tensor, torch.Tensor]]
    ],
    model_id: str,
    default_weights: str,
    weights_help_msg: str,
    app_type: Callable[..., YoloObjectDetectionApp],
    default_image: str,
    stride_multiple: int | None = None,
):
    # Demo parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--weights", type=str, default=default_weights, help=weights_help_msg
    )

    image_help = "image file path or URL."
    if stride_multiple:
        image_help = f"{image_help} Image spatial dimensions (x and y) must be multiples of {stride_multiple}."

    parser.add_argument("--image", type=str, default=default_image, help=image_help)
    parser.add_argument(
        "--score_threshold",
        type=float,
        default=0.45,
        help="Score threshold for NonMaximumSuppression",
    )
    parser.add_argument(
        "--iou_threshold",
        type=float,
        default=0.7,
        help="Intersection over Union (IoU) threshold for NonMaximumSuppression",
    )

    args = parser.parse_args()

    # Load image & model
    model = model_type.from_pretrained(args.weights)
    app = app_type(model, args.score_threshold, args.iou_threshold)
    print("Model Loaded")
    image = load_image(args.image, model_id)
    pred_images = app.predict_boxes_from_image(image)
    Image.fromarray(pred_images[0]).show()
