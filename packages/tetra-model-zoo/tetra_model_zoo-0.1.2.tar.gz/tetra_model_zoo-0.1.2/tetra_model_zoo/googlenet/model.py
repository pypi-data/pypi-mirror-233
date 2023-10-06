from __future__ import annotations

import torchvision.models as tv_models

from tetra_model_zoo.imagenet_classifier.model import ImagenetClassifier

MODEL_ID = __name__.split(".")[-2]
DEFAULT_WEIGHTS = "IMAGENET1K_V1"


class GoogLeNet(ImagenetClassifier):
    @staticmethod
    def from_pretrained(weights: str = PendingDeprecationWarning) -> ImagenetClassifier:
        net = tv_models.googlenet(weights=weights)
        return ImagenetClassifier(net)
