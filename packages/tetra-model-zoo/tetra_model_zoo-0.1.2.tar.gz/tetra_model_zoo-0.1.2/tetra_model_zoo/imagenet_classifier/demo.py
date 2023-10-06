import argparse
import json
from typing import Callable, Optional

import torch

from tetra_model_zoo.imagenet_classifier.app import ImagenetClassifierApp
from tetra_model_zoo.imagenet_classifier.model import MODEL_ID, ImagenetClassifier
from tetra_model_zoo.imagenet_classifier.test_utils import TEST_IMAGENET_IMAGE
from tetra_model_zoo.utils.asset_loaders import download_data, load_image

IMAGENET_LABELS_JSON = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
IMAGENET_LABELS_PATH = download_data(IMAGENET_LABELS_JSON, MODEL_ID)
with open(IMAGENET_LABELS_PATH, "r") as imagenet_file:
    IMAGENET_LABELS = json.load(imagenet_file)


#
# Run Imagenet Classifier end-to-end on a sample image.
# The demo will print the predicted class to terminal.
#
def imagenet_demo(
    model: Callable[..., ImagenetClassifier],
    default_weights: Optional[str],
    model_id: str,
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
        default=TEST_IMAGENET_IMAGE,
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
    app = ImagenetClassifierApp(model)
    probabilities = app.predict(image)
    predicted_class = torch.argmax(probabilities, dim=0)
    print(
        f"Prediction: {IMAGENET_LABELS[int(predicted_class)]}, {probabilities[predicted_class]}"
    )
