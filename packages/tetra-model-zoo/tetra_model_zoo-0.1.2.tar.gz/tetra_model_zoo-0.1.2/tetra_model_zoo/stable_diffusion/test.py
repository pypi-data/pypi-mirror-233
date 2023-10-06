import numpy as np
import pytest
from diffusers import StableDiffusionPipeline

from tetra_model_zoo.stable_diffusion.app import StableDiffusionApp
from tetra_model_zoo.stable_diffusion.model import (
    MODEL_ASSET_VERSION,
    MODEL_ID,
    SDTextEncoder,
    SDUNet,
    SDVAEDecoder,
)
from tetra_model_zoo.utils.asset_loaders import get_model_asset_url, load_image

IMAGE_ADDRESS = get_model_asset_url(
    MODEL_ID,
    MODEL_ASSET_VERSION,
    "CompVis-v1-4/a-high-quality-photo-of-a-surfing-dog-pytorch-seed42-steps2.png",
)


@pytest.mark.skip(reason="Uses a large amount of memory and is often killed by OOM.")
def test_e2e_numerical(
    monkeypatch,
):
    """
    Verify our PyTorch driver produces the correct image.
    """

    # Approve downloading the prerequisite GitHub repository.
    monkeypatch.setattr("builtins.input", lambda: "y")

    model_version = "CompVis/stable-diffusion-v1-4"
    prompt = "a high-quality photo of a surfing dog"
    # Not sufficient for a sensible image, but enough for a test.
    num_steps = 2
    seed = 42

    pipe = StableDiffusionPipeline.from_pretrained(model_version, use_auth_token=True)

    # Construct all the networks
    text_encoder = SDTextEncoder(pipe).eval()
    vae_decoder = SDVAEDecoder(pipe).eval()
    unet = SDUNet(pipe).eval()

    # Save the tokenizer and scheduler
    tokenizer = pipe.tokenizer
    scheduler = pipe.scheduler

    app = StableDiffusionApp(
        text_encoder=text_encoder,
        vae_decoder=vae_decoder,
        unet=unet,
        tokenizer=tokenizer,
        scheduler=scheduler,
    )

    ref_image_pil = load_image(IMAGE_ADDRESS, MODEL_ID)
    ref_image_np = np.array(ref_image_pil).astype(np.float32) / 255.0

    image = app.generate_image(prompt, num_steps=num_steps, seed=seed)

    np.allclose(image.detach().numpy(), ref_image_np)
