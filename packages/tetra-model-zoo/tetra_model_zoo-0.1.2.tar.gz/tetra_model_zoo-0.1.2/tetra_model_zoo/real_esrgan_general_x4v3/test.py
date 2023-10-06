import numpy as np

from tetra_model_zoo.real_esrgan_general_x4v3.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    Real_ESRGAN_General_x4v3,
)
from tetra_model_zoo.super_resolution.app import SuperResolutionApp
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image
from tetra_model_zoo.utils.testing import skip_clone_repo_check

IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "real_esrgan_general_x4v3_demo.jpg"
)
OUTPUT_IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "real_esrgan_general_x4v3_demo.png"
)


@skip_clone_repo_check
def test_realesrgan_app():
    image = load_image(IMAGE_ADDRESS, MODEL_ID)
    output_image = load_image(OUTPUT_IMAGE_ADDRESS, MODEL_ID)
    model = Real_ESRGAN_General_x4v3.from_pretrained()
    app = SuperResolutionApp(model)
    app_output_image = app.upscale_image(image)[0]
    np.testing.assert_allclose(
        np.asarray(app_output_image, dtype=np.float32),
        np.asarray(output_image, dtype=np.float32),
        rtol=0.02,
        atol=1.5,
    )
