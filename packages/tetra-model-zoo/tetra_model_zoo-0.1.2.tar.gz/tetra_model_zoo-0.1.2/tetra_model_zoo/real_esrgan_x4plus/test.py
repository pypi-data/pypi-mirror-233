import numpy as np

from tetra_model_zoo.real_esrgan_x4plus.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    Real_ESRGAN_x4plus,
)
from tetra_model_zoo.super_resolution.app import SuperResolutionApp
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image
from tetra_model_zoo.utils.testing import assert_most_same, skip_clone_repo_check

IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "real_esrgan_x4plus_demo.jpg"
)
OUTPUT_IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "real_esrgan_x4plus_demo_output.png"
)


@skip_clone_repo_check
def test_numerical():
    image = load_image(IMAGE_ADDRESS, MODEL_ID)
    model = Real_ESRGAN_x4plus.from_pretrained()
    app = SuperResolutionApp(model=model)
    output_img = app.upscale_image(image)[0]

    expected_output_image = load_image(OUTPUT_IMAGE_ADDRESS, MODEL_ID)
    assert_most_same(
        np.asarray(expected_output_image, dtype=np.float32),
        np.array(output_img).astype(np.float32),
        tolerance=0.01,
    )
