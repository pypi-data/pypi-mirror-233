import numpy as np
from PIL.Image import fromarray

from tetra_model_zoo.unet_segmentation.app import UNetSegmentationApp
from tetra_model_zoo.unet_segmentation.model import MODEL_ASSET_VERSION, MODEL_ID, UNet
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image

IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "unet_test_image.jpg"
)
OUTPUT_ADDRESS = get_model_asset_url(MODEL_ID, MODEL_ASSET_VERSION, "test_output.png")


def test_numerical():
    net = UNet.from_pretrained()

    img = load_image(IMAGE_ADDRESS, MODEL_ID)
    mask = UNetSegmentationApp(net).predict(img)

    # Convert raw mask of 0s and 1s into a PIL Image
    img = fromarray(mask)
    expected_out = load_image(OUTPUT_ADDRESS, MODEL_ID)
    np.testing.assert_allclose(np.array(img), np.array(expected_out))
