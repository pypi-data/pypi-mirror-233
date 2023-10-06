[![Tetra AI](https://tetra.ai/img/logo.svg)](https://tetra.ai/)

# [Stable Diffusion](https://tetra.ai/model-zoo/stable_diffusion)

Stable Diffusion is an AI image generator that takes as input a textual
description ("prompt") and produces an image.

The model consists of several neural network and non-neural network components:

  - Neural networks
    - Text Encoder: Converts the string into a numerical tensor
    - VAE Encoder: (optional) Converts an RGB image into a
      low-resolution/high-dimensionality representation
    - VAE Decoder: Converts the representation back to an RGB image
    - UNet: This runs one iteration of the diffusion process on the VAE-encoded
      image
    - Safety checker: (not included) Check if output image is NSFW. This is
      currently not included for export nor in the demo; may be required by the
      license depending on the use case.

  - Non-neural network components
    - Tokenizer: Splits text into tokens before embedded using the text encoder
    - Scheduler: Dictates the diffusion process

These are glued together in our demo as following:

  - The text encoder is run on the prompt, as well as an empty prompt
    (unconditional generation)
  - A noisy "image" (in the VAE embedded space) is randomly generated based on
    the seed
  - We enter the main diffusion loop.
  - The "image" is denoised using the UNet model guided by both text
    embeddings, as well as conditioned on the timestep.
  - The two slightly more denoised "images" (unconditional and conditional) are
    interpolated using the guidance scale to again form a single "image". The
    scheduler helps to scale this "image".
  - We go back to the main diffusion loop and repeat for as many steps as
    specified.
  - Finally, we decode the "image" into a real RGB image use the VAE Decoder.

Note that in this demo for brevity we did not make use the VAE Encoder (used
when conditioning on images) or the Safety checker (legally mandated when using
in a public-facing context).

More details, such as model latency and throughput running on various devices, can be found at https://tetra.ai/model-zoo/stable_diffusion

## Example & Usage

1. Install the package via pip:
```
pip install tetra_model_zoo[stable_diffusion]
```

2. Load the model & app
```
from tetra_model_zoo.stable_diffusion import Model
from tetra_model_zoo.stable_diffusion import App

app = App(Model.from_pretrained())
```

TODO: Update stable diffusion to use this application structure.

See [demo.py](demo.py) for sample usage of the model and app.

Please refer to our [general instructions on using models](../../#tetra-model-zoo) for more usage instructions.

## Optimize, Profile, and Validate Stable Diffusion for a device with Tetra Hub
Using Tetra Hub, you can easily optimize, profile, and validate Stable Diffusion for a device.

Run the following python script to export and optimize for iOS and Android:
```
python -m tetra_model_zoo.stable_diffusion.export [ --help ]
```

## Model In-Application Deployment instructions
<a href="mailto:support@tetra.ai?subject=Request Access for Tetra Hub&body=Interest in using Stable Diffusion in model zoo for deploying on-device.">Get in touch with us</a> to learn more!

## License
- Code in this repository is covered by the LICENSE file at the repository
  root.
- Stable Diffusion's license can be found
  [here](https://huggingface.co/spaces/CompVis/stable-diffusion-license).

## References
* [Arxiv Paper](https://arxiv.org/abs/2112.10752)
* [HuggingFace Repository](https://huggingface.co/CompVis/stable-diffusion-v1-4)
* [Apple Repository](https://github.com/apple/ml-stable-diffusion)
