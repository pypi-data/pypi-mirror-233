[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)

# [Real-ESRGAN-General-x4v3: Super-resolution of images optimised for mobile and edge](https://tetra.ai/model-zoo/real_esrgan_general_x4v3)

![](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/realesrgan/v1/realesrgan_demo.jpg)
to
![](https://tetra-public-assets.s3.us-west-2.amazonaws.com/model-zoo/realesrgan/v1/realesrgan_demo_output.png)

Real-ESRGAN is a machine learning model that upscales an image with no loss in quality.
We present an optimized implementation of the model suitable to export for mobile applications.
The implementation is a derivative of the Real-ESRGAN-General-x4v3 architecture, a smaller version
than the full Real-ESRGAN-x4plus architecture.

This is based on [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN). You can optionally
fine-tune the pre-trained model before walking through the examples below.

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/real_esrgan_general_x4v3

## Example & Usage

Install the package via pip:
```bash
pip install tetra_model_zoo[real_esrgan_general_x4v3]
```

See [demo.py](../super_resolution/demo.py) for model usage in Python.

Please refer to our [general instructions on using models](../../#tetra-model-zoo)

## Optimize, Profile, and Validate RealESRGAN for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate RealESRGAN for a device.

Run the following python script to export and optimize for iOS and Android:
```
python -m tetra_model_zoo.real_esrgan_general_x4v3.export [ --help ]
```

# Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using RealESRGAN in model zoo for deploying on-device.">Get in touch with us</a> to learn more!

## License
- Code in this repository is covered by the LICENSE file at the repository root.
- RealESRGAN's license can be found [here](https://github.com/xinntao/Real-ESRGAN/blob/master/LICENSE).
- [Demo image](https://www.flickr.com/photos/birds_and_critters/53102982569/) is public domain dedication licensed

## References
* [Whitepaper](https://arxiv.org/abs/2107.10833)
* [RealESRGAN Source Repository](https://github.com/xinntao/Real-ESRGAN)
