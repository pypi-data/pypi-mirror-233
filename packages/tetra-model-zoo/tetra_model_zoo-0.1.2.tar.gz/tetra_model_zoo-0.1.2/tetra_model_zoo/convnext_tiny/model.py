from __future__ import annotations

import torchvision.models as tv_models

from tetra_model_zoo.imagenet_classifier.model import ImagenetClassifier

MODEL_ID = __name__.split(".")[-2]
DEFAULT_WEIGHTS = "IMAGENET1K_V1"


class ConvNextTiny(ImagenetClassifier):
    @staticmethod
    def from_pretrained(weights: str = DEFAULT_WEIGHTS) -> ImagenetClassifier:
        net = tv_models.convnext_tiny(weights=weights)
        return ImagenetClassifier(net)
