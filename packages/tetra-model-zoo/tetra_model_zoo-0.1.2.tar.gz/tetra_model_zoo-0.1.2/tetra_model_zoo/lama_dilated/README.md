[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)

# [LaMa-Dilated: High resolution image in-painting optimized for mobile and edge](https://tetra.ai/model-zoo/lama_dilated)

LaMa-Dilated is a machine learning model that allows to erase and in-paint part of given input image.
We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on [LaMa-for-inpainting](https://github.com/advimman/lama/tree/main). You can optionally
fine-tune the pre-trained model before walking through the examples below.

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/lama_dilated

## Example & Usage
1. Install the package via pip:
```bash
pip install tetra_model_zoo[lama_dilated]
```

2. Run Demo (Note: This model may take a long time to load and run.)
```bash
python -m tetra_model_zoo.lama_dilated.demo [--help]
```

See [demo.py](../repaint/demo.py) for model usage in Python.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.

## Optimize, Profile, and Validate LaMa Dilated for a Device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate LaMa Dilated for a device.

Run the following python script to export and optimize for iOS and Android:
```
python -m tetra_model_zoo.lama_dilated.export [ --help ]
```

## Model In-Application Deployment Instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using LaMaDilated in model zoo for deploying on-device.">Get in touch with us</a> to learn more!

## License
- Code in this repository is covered by the LICENSE file at the repository root.
- LaMa Dilated's license can be found [here](https://github.com/advimman/lama/blob/main/LICENSE).

## References
* [Resolution-robust Large Mask Inpainting with Fourier Convolutions](https://arxiv.org/abs/2109.07161)
* [Source Repository](https://github.com/advimman/lama)
