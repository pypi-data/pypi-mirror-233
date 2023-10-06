import numpy as np

from tetra_model_zoo.mediapipe_pose.app import MediaPipePoseApp
from tetra_model_zoo.mediapipe_pose.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    MediaPipePose,
)
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image
from tetra_model_zoo.utils.testing import skip_clone_repo_check

INPUT_IMAGE_ADDRESS = get_model_asset_url(MODEL_ID, MODEL_ASSET_VERSION, "pose.jpeg")
OUTPUT_IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID, MODEL_ASSET_VERSION, "pose_output.png"
)


# Because we have not made a modification to the pytorch source network,
# no numerical tests are included for the model; only for the app.


@skip_clone_repo_check
def test_pose_app():
    input = load_image(
        INPUT_IMAGE_ADDRESS,
        MODEL_ID,
    )
    expected_output = load_image(
        OUTPUT_IMAGE_ADDRESS,
        MODEL_ID,
    ).convert("RGB")
    app = MediaPipePoseApp(MediaPipePose.from_pretrained())
    assert np.allclose(
        app.predict_landmarks_from_image(input)[0], np.asarray(expected_output)
    )
