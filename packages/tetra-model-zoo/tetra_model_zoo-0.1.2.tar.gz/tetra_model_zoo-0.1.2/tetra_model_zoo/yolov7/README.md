[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)

# [YoloV7: Real-time object detection optimized for mobile and edge](https://tetra.ai/model-zoo/yolov7)

YoloV7 is a machine learning model that predicts bounding boxes and classes of objects in an image.
We present an optimized implementation of the model suitable to export for low latency mobile applications.

This is based on [YOLOv7](https://github.com/WongKinYiu/yolov7). You can optionally
fine-tune the pre-trained model before walking through the examples below.

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/yolov7

## Example & Usage
1. Install the package via pip:
```bash
pip install tetra_model_zoo[yolov7]
```

2. Run the demo
```bash
python -m tetra_model_zoo.yolov7.demo [--help]
```

See [demo.py](../yolo/demo.py) for model usage in Python.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.

## Optimize, Profile, and Validate YOLOv7 for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate YOLOv7 for a device.

Run the following python script to export and optimize for iOS and Android:
```
python -m tetra_model_zoo.yolov7.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using YOLOv7 in model zoo for deploying on-device.">Get in touch with us</a> to learn more!

## License
- Code in this repository is covered by the LICENSE file at the repository root.
- YoloV7's license can be found [here](https://github.com/WongKinYiu/yolov7/blob/main/LICENSE.md).

## References
* [Whitepaper](https://arxiv.org/abs/2207.02696)
* [YoloV7 Source Repository](https://github.com/WongKinYiu/yolov7/)
