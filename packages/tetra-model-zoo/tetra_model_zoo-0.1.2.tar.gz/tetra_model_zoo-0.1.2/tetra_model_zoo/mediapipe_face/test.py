import numpy as np

from tetra_model_zoo.mediapipe_face.app import MediaPipeFaceApp
from tetra_model_zoo.mediapipe_face.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    MediaPipeFace,
)
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image
from tetra_model_zoo.utils.testing import skip_clone_repo_check

INPUT_IMAGE_ADDRESS = get_model_asset_url(MODEL_ID, MODEL_ASSET_VERSION, "face.jpeg")
OUTPUT_IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "face_output.png"
)


# Because we have not made a modification to the pytorch source network,
# no numerical tests are included for the model; only for the app.


@skip_clone_repo_check
def test_face_app():
    input = load_image(
        INPUT_IMAGE_ADDRESS,
        MODEL_ID,
    )
    expected_output = load_image(
        OUTPUT_IMAGE_ADDRESS,
        MODEL_ID,
    ).convert("RGB")
    app = MediaPipeFaceApp(MediaPipeFace.from_pretrained())
    assert np.allclose(
        app.predict_landmarks_from_image(input)[0], np.asarray(expected_output)
    )
