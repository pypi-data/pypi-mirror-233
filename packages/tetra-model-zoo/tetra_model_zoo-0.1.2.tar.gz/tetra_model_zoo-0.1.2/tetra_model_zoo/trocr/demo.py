import argparse
import time

from tetra_model_zoo.trocr.app import TrOCRApp
from tetra_model_zoo.trocr.model import (
    HUGGINGFACE_TROCR_MODEL,
    MODEL_ASSET_VERSION,
    MODEL_ID,
    TrOCR,
)
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image

HUGGINGFACE_TROCR_MODEL = "microsoft/trocr-small-stage1"
DEFAULT_SAMPLE_IMAGE = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "sample_text.jpg"
)

#
# Run TrOCR end-to-end on a sample line of handwriting.
# The demo will output the text contained within the source image.
# Text will be printed to terminal as it is generated with each decoder loop.
#


def main():
    # Demo parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image",
        type=str,
        default=DEFAULT_SAMPLE_IMAGE,
        help="image file path or URL",
    )
    parser.add_argument(
        "--hf_trocr_model",
        type=str,
        default=HUGGINGFACE_TROCR_MODEL,
        help=f"huggingface model to load. Tested with {HUGGINGFACE_TROCR_MODEL}.",
    )
    args = parser.parse_args()

    # Load Application
    app = TrOCRApp(TrOCR.from_pretrained(args.hf_trocr_model))

    # Load Image
    image = load_image(args.image, MODEL_ID)

    # Stream output from model
    print("\n** Predicted Text **\n")

    for output in app.stream_predicted_text_from_image(image):
        print(output[0], end="\r")
        # Sleep to accentuate the "streaming" affect in terminal output.
        time.sleep(0.1)

    print("\n")


if __name__ == "__main__":
    main()
