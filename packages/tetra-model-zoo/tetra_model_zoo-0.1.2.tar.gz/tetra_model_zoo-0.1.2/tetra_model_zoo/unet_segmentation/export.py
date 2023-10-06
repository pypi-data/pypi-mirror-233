from __future__ import annotations

from typing import Any, List

import torch

import tetra_hub as hub
from tetra_model_zoo.unet_segmentation.model import MODEL_ID, UNet
from tetra_model_zoo.utils.args import vision_export_parser
from tetra_model_zoo.utils.hub import download_hub_models


def trace(model: UNet, input_shape: List[int] = [1, 3, 224, 224]) -> Any:
    """
    Convert UNet to a pytorch trace. Traces can be saved and loaded from disk.
    Returns: Trace Object
    """
    return torch.jit.trace(model, [torch.ones(input_shape)])


def main():
    # Export parameters
    parser = vision_export_parser(
        default_x=224, default_y=224, dim_constraint="Must be >= 32."
    )

    args = parser.parse_args()

    # Instantiate the model and a sample input.
    unet = UNet.from_pretrained()

    assert args.x >= 32, "Width must be >=32."
    assert args.y >= 32, "Height must be >=32."

    # Trace the model.
    traced_model = trace(unet, [args.b, 3, args.y, args.x])

    # Select the device(s) you'd like to optimize for.
    devices = [hub.Device(x) for x in args.devices]

    # Submit the traced models for conversion and profiling.
    jobs = hub.submit_profile_job(
        name=MODEL_ID,
        model=traced_model,
        input_shapes=unet.get_input_spec(),
        device=devices,
    )

    # Download the optimized asset!
    download_hub_models(jobs)


if __name__ == "__main__":
    main()
