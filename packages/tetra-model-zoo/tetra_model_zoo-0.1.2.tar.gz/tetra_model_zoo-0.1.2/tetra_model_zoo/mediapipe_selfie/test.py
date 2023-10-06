import numpy as np

from tetra_model_zoo.mediapipe_selfie.app import SelfieSegmentationApp
from tetra_model_zoo.mediapipe_selfie.model import (
    DEFAULT_WEIGHTS,
    MODEL_ASSET_VERSION,
    MODEL_ID,
    SelfieSegmentation,
)
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image

IMAGE_ADDRESS = get_model_asset_url(MODEL_ID, MODEL_ASSET_VERSION, "selfie.jpg")
OUTPUT_IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "selfie_output.jpg"
)


def test_output():
    input_img = load_image(
        IMAGE_ADDRESS,
        MODEL_ID,
    )
    model = SelfieSegmentation.from_pretrained(DEFAULT_WEIGHTS)
    output = SelfieSegmentationApp(model).predict(input_img)
    expected_output = load_image(
        OUTPUT_IMAGE_ADDRESS,
        MODEL_ID,
    ).convert("L")

    expected_output = np.array(expected_output)
    np.testing.assert_allclose(
        np.round(np.asarray(expected_output, dtype=np.float32) / 255, 2),
        np.round(np.asarray(output, dtype=np.float32), 2),
        rtol=0.1,
        atol=0.1,
    )
