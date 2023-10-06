import numpy as np

from tetra_model_zoo.lama_dilated.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    LamaDilated,
)
from tetra_model_zoo.repaint.app import RepaintMaskApp
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image
from tetra_model_zoo.utils.testing import skip_clone_repo_check

IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "test_images/test_input_image.png"
)
MASK_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "test_images/test_input_mask.png"
)
OUTPUT_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "test_images/test_output.png"
)


@skip_clone_repo_check
def test_numerical():
    app = RepaintMaskApp(LamaDilated.from_pretrained())

    img = load_image(IMAGE_ADDRESS, MODEL_ID)
    mask_image = load_image(MASK_ADDRESS, MODEL_ID)
    out_img = app.paint_mask_on_image(img, mask_image)

    expected_out = load_image(OUTPUT_ADDRESS, MODEL_ID)

    np.testing.assert_allclose(
        np.asarray(out_img[0], dtype=np.float32),
        np.asarray(expected_out, dtype=np.float32),
        rtol=0.02,
        atol=1.5,
    )
