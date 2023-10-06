[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)

# [YoloV6: Real-time object detection optimized for mobile and edge](https://tetra.ai/model-zoo/yolov6)

YoloV6 is a machine learning model that predicts bounding boxes and classes of objects in an image.
We present an optimized implementation of the model suitable to export for low latency mobile applications.

This is based on [YOLOv6](https://github.com/meituan/YOLOv6/). You can optionally
fine-tune the pre-trained model before walking through the examples below.

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/yolov6

## Example & Usage
```bash
python -m tetra_model_zoo.yolov7.demo [--help]
```

See [demo.py](../yolo/demo.py) for model usage in Python.

## Optimize, Profile, and Validate YOLOv6 for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate YOLOv6 for a device.

Run the following python script to export and optimize for iOS and Android:
```
python -m tetra_model_zoo.yolov6.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using YOLOv6 in model zoo for deploying on-device.">Get in touch with us</a> to learn more!

## License
- Code in this repository is covered by the LICENSE file at the repository root.
- YoloV6's license can be found [here](https://github.com/meituan/YOLOv6/blob/47625514e7480706a46ff3c0cd0252907ac12f22/LICENSE).

## References
* [YOLOv6 v3.0: A Full-Scale Reloading](https://arxiv.org/abs/2301.05586)
* [YOLOv6: A Single-Stage Object Detection Framework for Industrial Applications](https://arxiv.org/abs/2209.02976)
* [YoloV6 Source Repository](https://github.com/meituan/YOLOv6/)
