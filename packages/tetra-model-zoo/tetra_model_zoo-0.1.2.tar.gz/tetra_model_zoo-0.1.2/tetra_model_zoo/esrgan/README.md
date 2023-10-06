[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)

# [ESRGAN: Super-resolution of images optimised for mobile and edge](https://tetra.ai/model-zoo/esrgan)

ESRGAN is a machine learning model that upscales an image with no loss in quality.
We present an optimized implementation of the model suitable to export for mobile applications.


This is based on [ESRGAN](https://github.com/xinntao/ESRGAN). You can optionally
fine-tune the pre-trained model before walking through the examples below.

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/esrgan

## Example and Usage
1. Install the package via pip:
```
pip install tetra_model_zoo[esrgan]
```

2. Load the model & app
```
from tetra_model_zoo.esrgan import Model
from tetra_model_zoo.esrgan import App

app = App(Model.from_pretrained())
```

3. Run prediction
```
from tetra_model_zoo.utils.asset_loaders import load_image
from tetra_model_zoo.esrgan.test import INPUT_IMAGE_ADDRESS
from tetra_model_zoo.esrgan import MODEL_ID

image = load_image(INPUT_IMAGE_ADDRESS, MODEL_ID)
app.predict(image)
```

See [demo.py](demo.py) for model usage in Python.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.

## Optimize, Profile, and Validate ESRGAN for a Device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate ESRGAN for a device.

Run the following python script to export and optimize for iOS and Android:
```
python -m tetra_model_zoo.esrgan.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using ESRGAN in model zoo for deploying on-device.">Get in touch with us</a> to learn more!

## License
- Code in this repository is covered by the LICENSE file at the repository root.
- ESRGAN's license can be found [here](https://github.com/xinntao/ESRGAN/blob/master/LICENSE).


## References
* [ESRGAN: Enhanced Super-Resolution Generative Adversarial Networks](https://arxiv.org/abs/1809.00219)
* [ESRGAN Source Repository](https://github.com/xinntao/ESRGAN)
