import argparse

from tetra_model_zoo.esr_gan.app import ESRGANApp
from tetra_model_zoo.esr_gan.model import ESRGAN, MODEL_ASSET_VERSION, MODEL_ID
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image


#
# Run ESRGAN end-to-end on a sample image.
# The demo will display a image upscaled with no loss in quality.
#
def main():
    # Demo parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image",
        type=str,
        default=get_model_asset_url(MODEL_ID, MODEL_ASSET_VERSION, "esrgan_demo.jpg"),
        help="image file path or URL.",
    )

    args = parser.parse_args()

    # Load image & model
    app = ESRGANApp(ESRGAN.from_pretrained())
    image = load_image(args.image, MODEL_ID)
    pred_images = app.upscale_image(image)
    pred_images.show()


if __name__ == "__main__":
    main()
