[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)

# [MediaPipe Selfie Segmentation](https://tetra.ai/model-zoo/mediapipe_selfie)

Light-weight model that segments a person from the background in square or landscape selfie and video conference imagery.

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/mediapipe_selfie

## Example & Usage

Install the package via pip:
```bash
pip install tetra_model_zoo[mediapipe_selfie]
```

See [demo.py](demo.py) for model usage in Python.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.

## Optimize, Profile, and Validate MediaPipe's Selfie Segmentation for a Device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate Mediapipe Selfie for a device.

Run the following python script to export and optimize for iOS and Android:
```
python -m tetra_model_zoo.mediapipe_selfie.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using MediaPipeSelfie in model zoo for deploying on-device.">Get in touch with us</a> to learn more!

## License
- Code in this repository is covered by the LICENSE file at the repository root.
- MediaPipe models's license can be found [here](https://github.com/google/mediapipe/blob/master/LICENSE)

## References
* [MediaPipe Selfie Segmentation Webpage](https://developers.google.com/mediapipe/solutions/vision/image_segmenter)
* [MediaPipe Selfie Segmentation Source Repository](https://github.com/google/mediapipe/tree/master/mediapipe/modules/selfie_segmentation)
