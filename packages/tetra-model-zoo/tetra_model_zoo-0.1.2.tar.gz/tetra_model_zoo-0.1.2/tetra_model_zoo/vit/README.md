[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)

# [VIT: Imagenet classifier and general purpose backbone optimized for mobile and edge](https://tetra.ai/model-zoo/vit)

VIT is a machine learning model that can classify images from the Imagenet dataset.
It can also be used as a backbone in building more complex models for specific use cases.
We present an optimized implementation of the model suitable to export and run on device.

This implementation is based on [VIT](https://github.com/pytorch/vision/blob/main/torchvision/models/vision_transformer.py). You can optionally
fine-tune the pre-trained model before walking through the examples below.

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/vit

## Example & Usage
See [demo.py](../imagenet_classifier/demo.py) for model usage in Python.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.

## Optimize, Profile, and Validate VIT for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate VIT for a device.

Run the following python script to export and optimize for iOS and Android:
```
python -m tetra_model_zoo.vit.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using VIT in model zoo for deploying on-device.">Get in touch with us</a> to learn more!

## License
- Code in this repository is covered by the LICENSE file at the repository root.
- VIT's license can be found [here](https://github.com/pytorch/vision/blob/main/LICENSE).

## References
* [An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929)
* [VIT Source Repository](https://github.com/pytorch/vision/blob/main/torchvision/models/vision_transformer.py)
