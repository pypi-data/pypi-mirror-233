[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)

# [InceptionNetV3: Imagenet classifier and general purpose backbone optimized for mobile and edge](https://tetra.ai/model-zoo/inception_v3)

InceptionNetV3 is a machine learning model that can classify images from the Imagenet dataset.
It can also be used as a backbone in building more complex models for specific use cases.
We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on [TorchVision's InceptionNetV3](https://github.com/pytorch/vision/blob/main/torchvision/models/inception.py). You can optionally
fine-tune the pre-trained model before walking through the examples below.

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/inception_v3

## Example & Usage
See [demo.py](../imagenet_classifier/demo.py) for model usage in Python.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.

## Optimize, Profile, and Validate InceptionNetV3 for a Device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate InceptionNetV3 for a device.

Run the following python script to export and optimize for iOS and Android:
```
python -m tetra_model_zoo.inception_v3.export [ --help ]
```

## Model In-Application Deployment Instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using InceptionV3 in model zoo for deploying on-device.">Get in touch with us</a> to learn more!

## License
- Code in this repository is covered by the LICENSE file at the repository root.
- InceptionNetV3's license can be found [here](https://github.com/pytorch/vision/blob/main/LICENSE).

## References
* [Rethinking the Inception Architecture for Computer Vision](http://arxiv.org/abs/1512.00567)
* [InceptionNetV3 Source Repository](https://github.com/pytorch/vision/blob/main/torchvision/models/inception.py)
