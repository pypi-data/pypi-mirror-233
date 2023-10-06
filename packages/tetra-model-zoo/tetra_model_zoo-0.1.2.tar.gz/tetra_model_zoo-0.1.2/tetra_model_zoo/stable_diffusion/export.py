from __future__ import annotations

import argparse

import torch
from diffusers import StableDiffusionPipeline

from tetra_model_zoo.stable_diffusion.model import (
    SDTextEncoder,
    SDUNet,
    SDVAEDecoder,
    SDVAEEncoder,
)
from tetra_model_zoo.utils.input_spec import make_torch_inputs

COMPONENTS = [
    "text_encoder",
    "vae_encoder",
    "vae_decoder",
    "unet",
]


# This is the mimimal set needed for the demo
DEFAULT_COMPONENTS = [
    "text_encoder",
    "vae_decoder",
    "unet",
]


def main():
    import tetra_hub as hub

    # Export parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--device",
        nargs="+",
        default=[
            "Apple iPhone 14 Pro",
        ],
        help="Device[s] to export to. Default: iPhone 14 Pro",
    )
    parser.add_argument(
        "--model_version",
        default="CompVis/stable-diffusion-v1-4",
        help="Pre-trained checkpoint and configuration. For available checkpoints: https://huggingface.co/models?search=stable-diffusion.",
    )
    parser.add_argument(
        "--components",
        nargs="+",
        choices=COMPONENTS,
        default=DEFAULT_COMPONENTS,
        help="Which components to export. Default: all models required for the demo.",
    )
    args = parser.parse_args()

    # Load model with weights from HuggingFace
    pipe = StableDiffusionPipeline.from_pretrained(
        args.model_version, use_auth_token=True
    )

    # Create Tetra Hub device objects
    devices = [hub.Device(device) for device in args.device]

    if "text_encoder" in args.components:
        text_encoder = SDTextEncoder(pipe).eval()

        # Construct input specifications and random inputs
        input_spec = text_encoder.get_input_spec()
        torch_inputs = [
            torch.randint(
                text_encoder.vocab_size, input_spec["input_ids"][0], dtype=torch.int32
            )
        ]

        # Trace the model
        traced_text_encoder = torch.jit.trace(text_encoder, torch_inputs)

        # Upload to Tetra Hub
        text_encoder_model = hub.upload_model(traced_text_encoder)

        # Submit a profile job to Tetra Hub
        hub.submit_profile_job(
            name="Stable Diffusion Text Encoder",
            model=text_encoder_model,
            input_shapes=input_spec,
            device=devices,
            options="--quantize_weight num_bits=16 --enable_mlpackage",
        )

    if "vae_encoder" in args.components:
        vae_encoder = SDVAEEncoder(pipe).eval()

        # Construct input specifications and random inputs
        input_spec = vae_encoder.get_input_spec()
        torch_inputs = make_torch_inputs(input_spec)

        # Trace the model
        traced_vae_encoder = torch.jit.trace(vae_encoder, torch_inputs)

        # Upload to Tetra Hub
        vae_encoder_model = hub.upload_model(traced_vae_encoder)

        # Submit a profile job to Tetra Hub
        hub.submit_profile_job(
            name="Stable Diffusion VAE Encoder",
            model=vae_encoder_model,
            input_shapes=input_spec,
            device=devices,
            options="--quantize_weight num_bits=16 --enable_mlpackage",
        )

    if "vae_decoder" in args.components:
        vae_decoder = SDVAEDecoder(pipe).eval()

        # Construct input specifications and random inputs
        input_spec = vae_decoder.get_input_spec()
        torch_inputs = make_torch_inputs(input_spec)

        # Trace the model
        traced_vae_decoder = torch.jit.trace(vae_decoder, torch_inputs)

        # Upload to Tetra Hub
        vae_decoder_model = hub.upload_model(traced_vae_decoder)

        # Submit a profile job to Tetra Hub
        hub.submit_profile_job(
            name="Stable Diffusion VAE Decoder",
            model=vae_decoder_model,
            input_shapes=input_spec,
            device=devices,
            options="--quantize_weight num_bits=16 --enable_mlpackage",
        )

    if "unet" in args.components:
        unet = SDUNet(pipe).eval()

        # Construct input specifications and random inputs
        input_spec = unet.get_input_spec()
        torch_inputs = make_torch_inputs(input_spec)

        # Trace the model
        traced_unet = torch.jit.trace(unet, torch_inputs)

        # Upload to Tetra Hub
        unet_model = hub.upload_model(traced_unet)

        # Submit a profile job to Tetra Hub
        hub.submit_profile_job(
            name="Stable Diffusion UNet",
            model=unet_model,
            input_shapes=input_spec,
            device=devices,
            options="--quantize_weight num_bits=8,method=linear --enable_mlpackage --max_profiler_iterations 1",
        )


if __name__ == "__main__":
    main()
