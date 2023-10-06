import numpy as np

from tetra_model_zoo.mediapipe_hand.app import MediaPipeHandApp
from tetra_model_zoo.mediapipe_hand.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    MediaPipeHand,
)
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image
from tetra_model_zoo.utils.testing import skip_clone_repo_check

INPUT_IMAGE_ADDRESS = get_model_asset_url(MODEL_ID, MODEL_ASSET_VERSION, "hand.jpeg")
OUTPUT_IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "hand_output.png"
)

# Because we have not made a modification to the pytorch source network,
# no numerical tests are included for the model; only for the app.


@skip_clone_repo_check
def test_hand_app():
    input = load_image(
        INPUT_IMAGE_ADDRESS,
        MODEL_ID,
    )
    expected_output = load_image(
        OUTPUT_IMAGE_ADDRESS,
        MODEL_ID,
    ).convert("RGB")
    app = MediaPipeHandApp(MediaPipeHand.from_pretrained())
    assert np.allclose(
        app.predict_landmarks_from_image(input)[0], np.asarray(expected_output)
    )
