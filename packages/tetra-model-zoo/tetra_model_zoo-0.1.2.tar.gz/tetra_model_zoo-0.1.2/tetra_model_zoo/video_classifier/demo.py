from __future__ import annotations

import argparse
from typing import Callable, Tuple

import torch

from tetra_model_zoo.utils.asset_loaders import download_data
from tetra_model_zoo.video_classifier.app import (
    KineticsClassifierApp,
    recognize_action_kinetics_400,
)


#
# Run KineticsClassifierApp end-to-end on a sample video.
# The demo will display top classification predictions for the video.
#
def kinetics_classifier_demo(
    model_type: Callable[
        ..., Callable[[torch.Tensor], Tuple[torch.Tensor, torch.Tensor, torch.Tensor]]
    ],
    model_id: str,
    default_weights: str,
    default_video: str,
):
    # Demo parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--weights",
        type=str,
        default=default_weights,
        help="Add weights for the model.",
    )

    parser.add_argument(
        "--video", type=str, default=default_video, help="video file path or URL."
    )

    args = parser.parse_args()

    # Load image & model
    model = model_type.from_pretrained(args.weights)
    app = KineticsClassifierApp(model)
    print("Model Loaded")
    dst_path = download_data(args.video, model_id)
    prediction = app.predict(path=dst_path)
    top5_classes = ",".join(recognize_action_kinetics_400(prediction))
    print(f"Top 5 predictions: {top5_classes}")
