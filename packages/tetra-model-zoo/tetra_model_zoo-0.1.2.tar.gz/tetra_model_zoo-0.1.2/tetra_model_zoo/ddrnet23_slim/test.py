import numpy as np

from tetra_model_zoo.ddrnet23_slim.app import DDRNetApp
from tetra_model_zoo.ddrnet23_slim.model import MODEL_ASSET_VERSION, MODEL_ID, DDRNet
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image
from tetra_model_zoo.utils.testing import assert_most_same, skip_clone_repo_check

INPUT_IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "test_input_image.png"
)
OUTPUT_IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "test_output_image.png"
)


# Verify that the output from Torch is as expected.
@skip_clone_repo_check
def test_numerical():
    app = DDRNetApp(DDRNet.from_pretrained())
    original_image = load_image(INPUT_IMAGE_ADDRESS, MODEL_ID)
    output_image = app.segment_image(original_image)[0]
    output_image_oracle = load_image(OUTPUT_IMAGE_ADDRESS, MODEL_ID)

    assert_most_same(
        np.asarray(output_image), np.asarray(output_image_oracle), tolerance=0.01
    )
