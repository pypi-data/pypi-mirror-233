[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)

# [MobileNetV3Small: Imagenet classifier and general purpose backbone optimized for mobile and edge](https://tetra.ai/model-zoo/mobilenet_v3_small)

MobileNetV3Small is a machine learning model that can classify images from the Imagenet dataset.
It can also be used as a backbone in building more complex models for specific use cases.
We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on [TorchVision's MobileNetV3Small](https://github.com/pytorch/vision/blob/main/torchvision/models/mobilenetv3.py). You can optionally
fine-tune the pre-trained model before walking through the examples below.

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/mobilenet_v3_small

## Example & Usage
See [demo.py](../imagenet_classifier/demo.py) for model usage in Python.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.

## Optimize, Profile, and Validate MobileNetV3Small for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate MobileNetV3Small for a device.

Run the following python script to export and optimize for iOS and Android:
```
python -m tetra_model_zoo.mobilenet_v3_small.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using MobileNetV3 Small in model zoo for deploying on-device.">Get in touch with us</a> to learn more!

## License
- Code in this repository is covered by the LICENSE file at the repository root.
- MobileNetV3Small's license can be found [here](https://github.com/pytorch/vision/blob/main/LICENSE).

## References
* [Searching for MobileNetV3](https://arxiv.org/abs/1905.02244)
* [MobileNetV3Small Source Repository](https://github.com/pytorch/vision/blob/main/torchvision/models/mobilenetv3.py)
