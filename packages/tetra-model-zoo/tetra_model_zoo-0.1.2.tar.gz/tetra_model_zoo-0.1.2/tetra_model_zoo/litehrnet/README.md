[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)

# [LiteHRNet: Real-time human pose detection of images optimized for mobile and edge](https://tetra.ai/model-zoo/litehrnet)

LiteHRNet is a machine learning model that detects human pose and returns a location and confidence
for each of 17 joints. We present an optimized implementation of the model suitable to export for mobile applications.

This is based on [LiteHRNet](https://github.com/HRNet/Lite-HRNet). You can optionally
fine-tune the pre-trained model before walking through the examples below.

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/litehrnet

## Example & Usage
1. Install the package via pip:
```bash
pip install tetra_model_zoo[litehrnet]
```

2. Run demo
```bash
python -m tetra_model_zoo.litehrnet.demo [--help]
```

See [demo.py](demo.py) for model usage in Python.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.

## Optimize, Profile, and Validate LiteHRNet for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate LiteHRNet for a device.

Run the following python script to export and optimize for iOS and Android:
```
python -m tetra_model_zoo.litehrnet.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using LiteHRNet in model zoo for deploying on-device.">Get in touch with us</a> to learn more!

## License
- Code in this repository is covered by the LICENSE file at the repository root.
- LiteHRNet's license can be found [here](https://github.com/HRNet/Lite-HRNet/blob/hrnet/LICENSE).

## References
* [Lite-HRNet: A Lightweight High-Resolution Network](https://arxiv.org/abs/2104.06403)
* [LiteHRNet Source Repository](https://github.com/HRNet/Lite-HRNet)
