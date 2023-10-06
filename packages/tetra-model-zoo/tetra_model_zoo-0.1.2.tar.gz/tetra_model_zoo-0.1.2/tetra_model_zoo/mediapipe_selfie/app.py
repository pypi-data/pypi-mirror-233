from typing import Callable

import numpy as np
import torch
from PIL import Image

from tetra_model_zoo.utils.image_processing import preprocess_PIL_image

RESIZE_SHAPE = (256, 256)


class SelfieSegmentationApp:
    """
    This class consists of light-weight "app code" that is required to
    perform end to end inference with UNet.

    For a given image input, the app will:
        * Pre-process the image (resize and normalize)
        * Run Selfie Segmentation model inference
        * Convert the raw output into segmented image.
    """

    def __init__(self, model: Callable[[torch.Tensor], torch.Tensor]):
        self.model = model

    def predict(self, image: Image) -> torch.Tensor:
        """
        From the provided image or tensor, generate the segmented mask.

        Parameters:
            image: A PIL Image in RGB format.

        Returns:
            mask: Segmented mask as np.array.
        """
        image = preprocess_PIL_image(image.resize(RESIZE_SHAPE))
        output = self.model(image)
        output = np.clip(np.reshape(output[0].detach().numpy(), (256, 256)), 0, 1)

        return output
