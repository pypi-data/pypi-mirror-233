[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)

# [AOT-GAN: High resolution image in-painting optimized for mobile and edge](https://tetra.ai/model-zoo/aotgan)

AOT-GAN is a machine learning model that allows to erase and in-paint part of given input image.
We present an optimized implementation of the model suitable to be exported for and run on device.

This is based on [AOT-GAN-for-inpainting](https://github.com/researchmm/AOT-GAN-for-Inpainting). You can optionally
fine-tune the pre-trained model before walking through the examples below.

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/aotgan

## Example and Usage
```bash
python -m tetra_model_zoo.aotgan.demo [--help]
```

See [demo.py](../repaint/demo.py) for model usage in Python.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.

## Optimize, Profile, and Validate AOT-GAN for a Device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate AOT-GAN for a device.

Run the following python script to export and optimize for iOS and Android:
```
python -m tetra_model_zoo.aotgan.export [ --help ]
```

## Model In-Application Deployment Instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using AOTGAN in model zoo for deploying on-device.">Get in touch with us</a> to learn more!

## License
- Code in this repository is covered by the LICENSE file at the repository root.
- The source AOT-GAN repository does not provide a license for their code.

## References
* [Aggregated Contextual Transformations for High-Resolution Image Inpainting](https://arxiv.org/abs/2104.01431
* [AOT-GAN Source Repository](https://github.com/researchmm/AOT-GAN-for-Inpainting)
