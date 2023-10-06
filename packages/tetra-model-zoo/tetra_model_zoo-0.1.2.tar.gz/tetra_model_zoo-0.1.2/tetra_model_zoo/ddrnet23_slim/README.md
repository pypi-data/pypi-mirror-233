[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)

# [DDRNet23-Slim: Real-time Semantic Segmentation optimized for mobile and edge](https://tetra.ai/model-zoo/DDRNet23-Slim)

DDRNet23Slim is a machine learning model that segments an image into semantic classes, specifically designed for road-based scenes. It is designed for the application of self-driving cars.
We present an optimized implementation of the model suitable to export for low latency mobile applications.

This is based on [DDRNet](https://github.com/chenjun2hao/DDRNet.pytorch). You can optionally
fine-tune the pre-trained model before walking through the examples below.

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/ddrnet23_slim/

## Example & Usage
python -m tetra_model_zoo.ddrnet23_slim.demo [--help]
```

See [demo.py](demo.py) for model usage in Python.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.

## Optimize, Profile, and Validate DDRNet for a Device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate DDRNet for a device.

Run the following python script to export and optimize for iOS and Android:
```
python -m tetra_model_zoo.ddrnet23_slim.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using DDRNet23-Slim in model zoo for deploying on-device.">Get in touch with us</a> to learn more!

## License
- Code in this repository is covered by the LICENSE file at the repository root.
- DDRNet's license can be found [here](https://github.com/chenjun2hao/DDRNet.pytorch/blob/main/LICENSE).

## References
* [Deep Dual-resolution Networks for Real-time and
Accurate Semantic Segmentation of Road Scenes](https://arxiv.org/abs/2101.06085)
* [DDRNet Source Repository](https://github.com/chenjun2hao/DDRNet.pytorch)
