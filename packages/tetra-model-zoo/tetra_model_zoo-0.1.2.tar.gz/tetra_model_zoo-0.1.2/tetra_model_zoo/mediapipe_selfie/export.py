from __future__ import annotations

from typing import Any, List

import torch

import tetra_hub as hub
from tetra_model_zoo.mediapipe_selfie.model import SelfieSegmentation
from tetra_model_zoo.utils.args import base_export_parser
from tetra_model_zoo.utils.hub import download_hub_models


def trace(model: SelfieSegmentation, input_shape: List[int]) -> Any:
    """
    Convert Selfie Segmentation to a pytorch trace. Traces can be saved & loaded from disk.
    Returns: Trace Object
    """
    return torch.jit.trace(model, [torch.ones(input_shape)])


def main():
    # Export parameters
    parser = base_export_parser()
    parser.add_argument(
        "--image_type",
        type=str,
        default="square",
        choices=["square", "landscape"],
        help="Pick between square or landscape model type.",
    )

    args = parser.parse_args()
    if args.image_type == "square":
        image_height, image_width = 256, 256
    else:
        image_height, image_width = 144, 256

    # Instantiate the model & a sample input.
    mediapipe_selfie_model = SelfieSegmentation.from_pretrained(args.image_type)

    # Trace the model.
    traced_mediapipe_selfie = trace(
        mediapipe_selfie_model, [1, 3, image_height, image_width]
    )

    # Select the device(s) you'd like to optimize for.
    devices = [hub.Device(x) for x in args.devices]

    # Submit the traced models for conversion & profiling.
    jobs = hub.submit_profile_job(
        name="mediapipe_selfie_seg",
        model=traced_mediapipe_selfie,
        input_shapes={"image": ((1, 3, image_height, image_width), "float32")},
        device=devices,
    )

    # Download the optimized assets!
    download_hub_models(jobs)


if __name__ == "__main__":
    main()
