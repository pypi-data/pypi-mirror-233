[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)

# [MediaPipe Pose: Detect and track human body poses in real-time images and video streams](https://tetra.ai/model-zoo/mediapipe_pose)

The MediaPipe Pose Landmark Detector is a machine learning pipeline that predicts bounding boxes and pose skeletons of poses in an image.
We present an optimized implementation suitable to export for low latency mobile applications.

This is based on [MediaPipe PyTorch](https://github.com/zmurez/MediaPipePyTorch). You can optionally
fine-tune the pre-trained model before walking through the examples below.

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/mediapipe_pose

## Example & Usage
1. Install the package via pip:
```
pip install tetra_model_zoo[mediapipe_pose]
```

2. Load the model & app
```
from tetra_model_zoo.mediapipe_pose import Model
from tetra_model_zoo.mediapipe_pose import App

# check demo.py for more details
app = App(Model.from_pretrained())
```

3. Run prediction
```
from tetra_model_zoo.utils.asset_loaders import load_image
from tetra_model_zoo.mediapipe_pose.test import INPUT_IMAGE_ADDRESS
from tetra_model_zoo.mediapipe_pose import MODEL_ID

image = load_image(INPUT_IMAGE_ADDRESS, MODEL_ID)
app.predict(image)
```

See [demo.py](demo.py) for model usage in Python.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.

## Optimize, Profile, and Validate MediaPipe Pose for a Device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate the MediaPipe Pose pipeline for a device.

Run the following python script to export and optimize for iOS and Android:
```
python -m tetra_model_zoo.mediapipe_pose.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using MediaPipePose in model zoo for deploying on-device.">Get in touch with us</a> to learn more!

## License
- Code in this repository is covered by the LICENSE file at the repository root.
- MediaPipe's license can be found [here](https://github.com/google/MediaPipe/blob/master/LICENSE).
- MediaPipe Pytorch's license can be found [here](https://github.com/zmurez/MediaPipePyTorch/blob/master/LICENSE)

## References
* [BlazePose: On-device Real-time Body Pose tracking](https://arxiv.org/abs/2006.10204)
* [MediaPipe Repository](https://github.com/google/MediaPipe/)
* [MediaPipe PyTorch Repository](https://github.com/zmurez/MediaPipePyTorch/)
