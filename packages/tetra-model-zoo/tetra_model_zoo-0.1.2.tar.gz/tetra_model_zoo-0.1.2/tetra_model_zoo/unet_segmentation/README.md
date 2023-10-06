[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)

# [UNet: Image Segmentation optimized for mobile and edge](https://tetra.ai/model-zoo/unet_segmentation)

UNet is a machine learning model that produces a segmentation mask for an image.
The most basic use case will label each pixel in the image as being in the foreground or the
background. More advanced usage will assign a class label to each pixel.

We present an optimized implementation of the model suitable to export for low latency mobile applications.

This is based on [UNet](https://github.com/milesial/Pytorch-UNet). You can optionally
fine-tune the pre-trained model before walking through the examples below.

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/unet_segmentation

## Example & Usage

Install the package via pip:
```bash
pip install tetra_model_zoo[unet_segmentation]
```

See [demo.py](demo.py) for model usage in Python.

## Optimize, Profile, and Validate Unet for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate Unet for a device.

Run the following python script to export and optimize for iOS and Android:
```bash
python -m tetra_model_zoo.unet_segmentation.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using Unet in model zoo for deploying on-device.">Get in touch with us</a> to learn more!

## License
- Code in this repository is covered by the LICENSE file at the repository root.
- UNet's license can be found [here](https://github.com/milesial/Pytorch-UNet/blob/master/LICENSE).

## References
* [U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)
* [UNet Source Repository](https://github.com/milesial/Pytorch-UNet)
