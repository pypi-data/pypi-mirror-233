[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)

# Tetra Model Zoo
The [Tetra Model Zoo](https://tetra.ai/model-zoo) is a collection of state-of-the-art models optimized for performance and memory and ready to deploy on mobile or edge.

# About Tetra
Tetra (https://tetra.ai) is a team of engineers and researchers dedicated to the democratization of Machine Learning on the edge.

Tetra Hub (https://hub.tetra.ai/) can export any PyTorch model to run on-device in minutes, running with industry-leading low latency via Tetra Runtime.

Our goal to make edge deployment as attainable, easy, and fast as possible. Performance for each model can be found at https://tetra.ai/model-zoo.

## Installation

We recommend using a virtual environment to use the model zoo (conda or virtual-env).

```
python -m venv model_zoo_env && source model_zoo_env/bin/activate
```

This repository is tested with python 3.8+

### Install from PyPi
```bash
pip install tetra_model_zoo
```
Some models require additional dependencies (see model README for details). To install those additional dependencies:
```bash
pip install tetra_model_zoo[trocr]
```

### Install from source
```bash
git clone git@github.com:tetraai/model-zoo.git
cd model-zoo
pip install -e .
```
Install additional dependencies to prepare a model before using, e.g.
```bash
pip install -e ".[trocr]"
```

## Getting Started

### CLI Demos
[All models](#model-directory) contain CLI-based demos that run the model end ***(in PyTorch)*** to end with sample input.
```bash
python -m tetra_model_zoo.trocr.demo [--help]
```
***Demos are optimized for code clarity rather than latency, and run exclusively in PyTorch. Optimal model latency can be achieved with model export via Tetra Hub.***

**See the [model directory](#model-directory) below to explore all other models.**

---

### Exportable PyTorch Models
An exportable PyTorch implementation of each model is provided.

```python
from tetra_model_zoo.trocr import Model
model = Model.from_pretrained() # Model is a PyTorch Module
```

Many models may have initialization parameters that allow loading custom weights and checkpoints.

---

### End to End Model Applications
Most ML use cases require some pre and post-processing that are not part of the model itself.

An python reference implementation of this is provided for each model. We call these reference implementation `app`s.
Apps load & preprocess model input, run model inference, and postprocess model output before returning it to you.

```python
from PIL import Image
from tetra_model_zoo.yolov7 import Model
from tetra_model_zoo.yolov7 import App
from tetra_model_zoo.utils.asset_loaders import load_image
from tetra_model_zoo.yolov7.test import IMAGE_ADDRESS

app = App(Model.from_pretrained())
image = load_image(IMAGE_ADDRESS)
image = app.predict(image) # Each model's application is executed differently. See each model's README & demo for more details.
Image.fromarray(pred_images[0]).show()
```

---

### Export models to run on device with Tetra Hub
Using Tetra Hub, any zoo model can be exported to run on device:

```bash
# Export will create and download compiled assets that will run on iOS and Android.
python -m tetra_model_zoo.trocr.export [--help]
```

**To use Tetra Hub, credentials are required**. [Get in touch with us](mailto:support@tetra.ai) to learn more!

---

### Tests
All models have accuracy and end-to-end tests when applicable.
To run the tests for a model:

```bash
python -m pytest --pyargs tetra_model_zoo.trocr.test
```

---

## Model Directory

### Computer Vision

| Model | README | Torch App | Device Export | CLI Demo
| -- | -- | -- | -- | --
| | | | |
| **Image Classification**
| [ResNet50](https://tetra.ai/model-zoo/resnet50) | [tetra_model_zoo.resnet50](tetra_model_zoo/resnet50/README.md) | ✔️ | ✔️ | ✔️
| [MobileNet-v3-Large](https://tetra.ai/model-zoo/mobilenet_v3_large) | [tetra_model_zoo.mobilenet_v3_large](tetra_model_zoo/mobilenet_v3_large/README.md) | ✔️ | ✔️ | ✔️
| [GoogLeNet](https://tetra.ai/model-zoo/googlenet) | [tetra_model_zoo.googlenet](tetra_model_zoo/googlenet/README.md) | ✔️ | ✔️ | ✔️
| [WideResNet50](https://tetra.ai/model-zoo/wideresnet50) | [tetra_model_zoo.wideresnet50](tetra_model_zoo/wideresnet50/README.md) | ✔️ | ✔️ | ✔️
| [ResNeXt50](https://tetra.ai/model-zoo/resnext50) | [tetra_model_zoo.resnext50](tetra_model_zoo/resnext50/README.md) | ✔️ | ✔️ | ✔️
| [MobileNet-v3-Small](https://tetra.ai/model-zoo/mobilenet_v3_small) | [tetra_model_zoo.mobilenet_v3_small](tetra_model_zoo/mobilenet_v3_small/README.md) | ✔️ | ✔️ | ✔️
| [MNASNet05](https://tetra.ai/model-zoo/mnasnet05) | [tetra_model_zoo.mnasnet05](tetra_model_zoo/mnasnet05/README.md) | ✔️ | ✔️ | ✔️
| [SqueezeNet-1_1](https://tetra.ai/model-zoo/squeezenet1_1) | [tetra_model_zoo.squeezenet1_1](tetra_model_zoo/squeezenet1_1/README.md) | ✔️ | ✔️ | ✔️
| [ConvNext-Tiny](https://tetra.ai/model-zoo/convnext_tiny) | [tetra_model_zoo.convnext_tiny](tetra_model_zoo/convnext_tiny/README.md) | ✔️ | ✔️ | ✔️
| [Densenet-121](https://tetra.ai/model-zoo/densenet121) | [tetra_model_zoo.densenet121](tetra_model_zoo/densenet121/README.md) | ✔️ | ✔️ | ✔️
| [Inception-v3](https://tetra.ai/model-zoo/inception_v3) | [tetra_model_zoo.inception_v3](tetra_model_zoo/inception_v3/README.md) | ✔️ | ✔️ | ✔️
| [EfficientNet-B0](https://tetra.ai/model-zoo/efficientnet_b0) | [tetra_model_zoo.efficientnet_b0](tetra_model_zoo/efficientnet_b0/README.md) | ✔️ | ✔️ | ✔️
| [ResNeXt101](https://tetra.ai/model-zoo/resnext101) | [tetra_model_zoo.resnext101](tetra_model_zoo/resnext101/README.md) | ✔️ | ✔️ | ✔️
| [VIT](https://tetra.ai/model-zoo/vit) | [tetra_model_zoo.vit](tetra_model_zoo/vit/README.md) | ✔️ | ✔️ | ✔️
| [MobileNet-v2](https://tetra.ai/model-zoo/mobilenet_v2) | [tetra_model_zoo.mobilenet_v2](tetra_model_zoo/mobilenet_v2/README.md) | ✔️ | ✔️ | ✔️
| [RegNet](https://tetra.ai/model-zoo/regnet) | [tetra_model_zoo.regnet](tetra_model_zoo/regnet/README.md) | ✔️ | ✔️ | ✔️
| | | | |
| **Image Editing**
| [AOT-GAN](https://tetra.ai/model-zoo/aotgan) | [tetra_model_zoo.aotgan](tetra_model_zoo/aotgan/README.md) | ✔️ | ✔️ | ✔️
| [LaMa-Dilated](https://tetra.ai/model-zoo/lama_dilated) | [tetra_model_zoo.lama_dilated](tetra_model_zoo/lama_dilated/README.md) | ✔️ | ✔️ | ✔️
| | | | |
| **Super Resolution**
| [Real-ESRGAN-General-x4v3](https://tetra.ai/model-zoo/real_esrgan_general_x4v3) | [tetra_model_zoo.real_esrgan_general_x4v3](tetra_model_zoo/real_esrgan_general_x4v3/README.md) | ✔️ | ✔️ | ✔️
| [Real-ESRGAN-x4plus](https://tetra.ai/model-zoo/real_esrgan_x4plus) | [tetra_model_zoo.real_esrgan_x4plus](tetra_model_zoo/real_esrgan_x4plus/README.md) | ✔️ | ✔️ | ✔️
| [ESRGAN](https://tetra.ai/model-zoo/esrgan) | [tetra_model_zoo.esrgan](tetra_model_zoo/esrgan/README.md) | ✔️ | ✔️ | ✔️
| | | | |
| **Segmentation**
| [Segment-Anything-Model](https://tetra.ai/model-zoo/sam) | [tetra_model_zoo.sam](tetra_model_zoo/sam/README.md) | ✔️ | ✔️ | ✔️
| [MediaPipe-Selfie-Segmentation](https://tetra.ai/model-zoo/mediapipe_selfie) | [tetra_model_zoo.mediapipe_selfie](tetra_model_zoo/mediapipe_selfie/README.md) | ✔️ | ✔️ | ✔️
| [Unet-Segmentation](https://tetra.ai/model-zoo/unet_segmentation) | [tetra_model_zoo.unet_segmentation](tetra_model_zoo/unet_segmentation/README.md) | ✔️ | ✔️ | ✔️
| | | | |
| **Semantic Segmentation**
| [DDRNet23-Slim](https://tetra.ai/model-zoo/ddrnet23_slim) | [tetra_model_zoo.ddrnet23_slim](tetra_model_zoo/ddrnet23_slim/README.md) | ✔️ | ✔️ | ✔️
| | | | |
| **Object Detection**
| [Yolo-v6](https://tetra.ai/model-zoo/yolov6) | [tetra_model_zoo.yolov6](tetra_model_zoo/yolov6/README.md) | ✔️ | ✔️ | ✔️
| [Yolo-v7](https://tetra.ai/model-zoo/yolov7) | [tetra_model_zoo.yolov7](tetra_model_zoo/yolov7/README.md) | ✔️ | ✔️ | ✔️
| [Yolo-v8-Detection](https://tetra.ai/model-zoo/yolov8_det) | [tetra_model_zoo.yolov8_det](tetra_model_zoo/yolov8_det/README.md) | ✔️ | ✔️ | ✔️
| [MediaPipe-Face-Detection](https://tetra.ai/model-zoo/mediapipe_face) | [tetra_model_zoo.mediapipe_face](tetra_model_zoo/mediapipe_face/README.md) | ✔️ | ✔️ | ✔️
| [MediaPipe-Hand-Detection](https://tetra.ai/model-zoo/mediapipe_hand) | [tetra_model_zoo.mediapipe_hand](tetra_model_zoo/mediapipe_hand/README.md) | ✔️ | ✔️ | ✔️
| | | | |
| **Pose Estimation**
| [MediaPipe-Pose-Estimation](https://tetra.ai/model-zoo/mediapipe_pose) | [tetra_model_zoo.mediapipe_pose](tetra_model_zoo/mediapipe_pose/README.md) | ✔️ | ✔️ | ✔️
| [LiteHRNet](https://tetra.ai/model-zoo/litehrnet) | [tetra_model_zoo.litehrnet](tetra_model_zoo/litehrnet/README.md) | ✔️ | ✔️ | ✔️

### Audio

| Model | README | Torch App | Device Export | CLI Demo
| -- | -- | -- | -- | --
| | | | |
| **Speech Recognition**
| [Whisper-Base](https://tetra.ai/model-zoo/whisper_asr) | [tetra_model_zoo.whisper_asr](tetra_model_zoo/whisper_asr/README.md) | ✔️ | ✔️ | ✔️

### Multimodal

| Model | README | Torch App | Device Export | CLI Demo
| -- | -- | -- | -- | --
| | | | |
| [OpenAI-Clip](https://tetra.ai/model-zoo/openai_clip) | [tetra_model_zoo.openai_clip](tetra_model_zoo/openai_clip/README.md) | ✔️ | ✔️ | ✔️
| [Optimized-Clip](https://tetra.ai/model-zoo/optimized_clip) | [tetra_model_zoo.optimized_clip](tetra_model_zoo/optimized_clip/README.md) | ✔️ | ✔️ | ✔️
| [TrOCR](https://tetra.ai/model-zoo/trocr) | [tetra_model_zoo.trocr](tetra_model_zoo/trocr/README.md) | ✔️ | ✔️ | ✔️
