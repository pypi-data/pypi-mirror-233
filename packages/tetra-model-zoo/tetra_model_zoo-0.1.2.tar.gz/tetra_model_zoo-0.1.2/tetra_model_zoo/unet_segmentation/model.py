from __future__ import annotations

from typing import Optional

import torch

from tetra_model_zoo.utils.asset_loaders import download_data
from tetra_model_zoo.utils.input_spec import InputSpec

MODEL_ID = __name__.split(".")[-2]
MODEL_REPO = "milesial/Pytorch-UNet"
MODEL_TYPE = "unet_carvana"
MODEL_ASSET_VERSION = 1
DEFAULT_WEIGHTS = "https://github.com/milesial/Pytorch-UNet/releases/download/v3.0/unet_carvana_scale1.0_epoch2.pth"


class UNet(torch.nn.Module):
    def __init__(self, net: torch.nn.Module) -> None:
        super().__init__()
        self.net = net

    @staticmethod
    def from_pretrained(ckpt_url: Optional[str] = DEFAULT_WEIGHTS):
        net = torch.hub.load(
            MODEL_REPO, MODEL_TYPE, pretrained=False, scale=1.0, trust_repo=True
        )
        if ckpt_url is not None:
            ckpt_path = download_data(DEFAULT_WEIGHTS, MODEL_ID)
            state_dict = torch.load(ckpt_path, map_location="cpu")
            net.load_state_dict(state_dict)
        return UNet(net.eval())

    def forward(self, image: torch.Tensor):
        """
        Run UNet on `image`, and produce a segmentation mask over the image.

        Parameters:
            image: A [1, 3, H, W] image.
                   The smaller of H, W should be >= 16, the larger should be >=32
                   Pixel values pre-processed for encoder consumption.
                   Range: float[0, 1]
                   3-channel Color Space: RGB

        Returns:
            mask: Shape [1, n_classes, H, W] where H, W are the same as the input image.
                  n_classes is 2 for the default model.

                  Each channel represents the raw logit predictions for a given class.
                  Taking the softmax over all channels for a given pixel gives the
                  probability distribution over classes for that pixel.
        """
        return self.net(image)

    def get_input_spec(
        self,
        image_size: tuple[int, int] | int = 224,
        batch_size: int = 1,
        num_channels: int = 3,
    ) -> InputSpec:
        """
        Returns the input specification (name -> (shape, type). This can be
        used to submit profiling job on TetraHub.
        """
        if isinstance(image_size, int):
            image_size = (image_size, image_size)
        return {"image": ((batch_size, num_channels, *image_size), "float32")}
