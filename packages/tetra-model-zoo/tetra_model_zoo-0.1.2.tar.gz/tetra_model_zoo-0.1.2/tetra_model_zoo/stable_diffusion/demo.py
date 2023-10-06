import argparse

import numpy as np
from diffusers import StableDiffusionPipeline
from PIL import Image

from tetra_model_zoo.stable_diffusion.app import StableDiffusionApp
from tetra_model_zoo.stable_diffusion.model import SDTextEncoder, SDUNet, SDVAEDecoder

DEFAULT_DEMO_PROMPT = "a high-quality photo of a surfing dog"


#
# Run Stable Diffuison end-to-end on a given prompt. The demo will output an
# AI-generated image based on the description in the prompt.
#
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt",
        default=DEFAULT_DEMO_PROMPT,
        help="Prompt to generate image from.",
    )
    parser.add_argument(
        "--model_version",
        default="CompVis/stable-diffusion-v1-4",
        help="Pre-trained checkpoint and configuration. For available checkpoints: https://huggingface.co/models?search=stable-diffusion.",
    )
    parser.add_argument(
        "--num_steps",
        default=50,
        type=int,
        help="The number of diffusion iteration steps (higher means better quality).",
    )
    parser.add_argument(
        "--seed",
        default=0,
        type=int,
        help="Random seed.",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Path to output file. By default show it interactively.",
    )
    parser.add_argument(
        "--guidance_scale",
        type=float,
        default=7.5,
        help="Strength of guidance (higher means more influence from prompt).",
    )
    args = parser.parse_args()

    # Load components

    # Load model with weights from HuggingFace
    pipe = StableDiffusionPipeline.from_pretrained(
        args.model_version, use_auth_token=True
    )

    # Construct all the networks
    text_encoder = SDTextEncoder(pipe).eval()
    vae_decoder = SDVAEDecoder(pipe).eval()
    unet = SDUNet(pipe).eval()

    # Save the tokenizer and scheduler
    tokenizer = pipe.tokenizer
    scheduler = pipe.scheduler

    # Load Application
    app = StableDiffusionApp(
        text_encoder=text_encoder,
        vae_decoder=vae_decoder,
        unet=unet,
        tokenizer=tokenizer,
        scheduler=scheduler,
    )

    print()
    print("** Performing image generation with Stable Diffusion **")
    print()
    print("Prompt:", args.prompt)
    print("Model:", args.model_version)
    print("Number of steps:", args.num_steps)
    print("Guidance scale:", args.guidance_scale)
    print("Seed:", args.seed)
    print()
    print(
        "Note: This reference demo uses significant amounts of memory and may take a few minutes to run."
    )
    print()

    # Generate image
    image = app.generate_image(
        args.prompt,
        num_steps=args.num_steps,
        seed=args.seed,
        guidance_scale=args.guidance_scale,
    )

    pil_img = Image.fromarray(np.round(image.detach().numpy() * 255).astype(np.uint8))

    # Save or show image
    if args.output is None:
        pil_img.show()
    else:
        pil_img.save(args.output)
        print()
        print("Image saved to", args.output)
        print()


if __name__ == "__main__":
    main()
