import gc

import diffusers
import numpy as np
import torch
import transformers
from tqdm import tqdm

from tetra_model_zoo.stable_diffusion.model import SDTextEncoder, SDUNet, SDVAEDecoder


class StableDiffusionApp:
    """
    StableDiffusionApp represents the application code needed to string
    together the various neural networks that make up the Stable Diffusion
    algorithm. This code is written in Python and uses PyTorch and is meant to
    serve as a reference implementation for application in other languages and
    for other platforms.

    Please run the app via `demo.py`.

    References
    ----------
    * https://arxiv.org/abs/2112.10752
    * https://github.com/apple/ml-stable-diffusion
    """

    def __init__(
        self,
        text_encoder: SDTextEncoder,
        vae_decoder: SDVAEDecoder,
        unet: SDUNet,
        tokenizer: transformers.SpecialTokensMixin,
        scheduler: diffusers.SchedulerMixin,
    ):

        self.text_encoder = text_encoder
        self.vae_decoder = vae_decoder
        self.unet = unet
        self.tokenizer = tokenizer
        self.scheduler = scheduler

    def _encode_text_prompt(
        self, prompt: str, do_classifier_free_guidance: bool = False
    ) -> torch.Tensor:
        """
        Takes a text prompt and returns a tensor with its text embedding.

        Parameters
        ----------
        prompt : str
            The text prompt to encode.
        do_classifier_free_guidance : bool
            Whether to use classifier-free guidance. If True, the returned text
            embedding will be a batch of two, with the unconditional and the
            conditional embeddings.
        """
        # Tokenize
        text_input = self.tokenizer(
            prompt,
            padding="max_length",
            max_length=self.tokenizer.model_max_length,
            return_tensors="pt",
        )

        # Embed using the text encoder neural network
        text_embeddings, _ = self.text_encoder(text_input.input_ids)

        if do_classifier_free_guidance:
            # Unconditional prompt is simply an empty string
            uncond_prompt = ""

            # Tokenize
            uncond_input = self.tokenizer(
                uncond_prompt,
                padding="max_length",
                max_length=self.tokenizer.model_max_length,
                truncation=True,
                return_tensors="pt",
            )

            # Embed using the text encoder neural network
            uncond_embeddings, _ = self.text_encoder(uncond_input.input_ids)

            # The text embeddings becomes a batch of two
            text_embeddings = torch.cat([uncond_embeddings, text_embeddings], dim=0)

        # Transpose to (batch_size, embedding_size, 1, sequence_length)
        text_embeddings = text_embeddings.permute(0, 2, 1).unsqueeze(2)

        return text_embeddings

    def predict(self, *args, **kwargs):
        # See generate_image.
        return self.generate_image(*args, **kwargs)

    def generate_image(
        self,
        prompt: str,
        num_steps: int = 50,
        seed: int = 0,
        guidance_scale: float = 7.5,
    ) -> torch.Tensor:
        """
        Generate an image using the PyTorch reference neural networks. This
        code can be used as a reference for how to glue together the neural
        networks in an application. Note that this code relies on a tokenizer
        and scheduler from the HuggingFace's diffusers library, so those would
        have to be ported to the application as well.

        Parameters
        ----------
        prompt : str
            The text prompt to generate an image from.
        num_steps : int
            The number of steps to run the diffusion process for. Higher value
            may lead to better image quality.
        seed : int
            The seed to use for the random number generator.
        guidance_scale : float
            Classifier-free guidance is a method that allows us to control how
            strongly the image generation is guided by the prompt. This is done
            by always processing two samples at once: an unconditional (using a
            text embedding of an empty prompt) and a conditional (using a text
            embedding of the provided prompt). Given the noise prediction of
            both of these, we linearly interpolate between them based on the
            guidance_scale. A guidance scale of 0 is the same as using an empty
            prompt. A guidance scale of 1 turns off classifier-free guidance
            and is computationally less expensive since it only processes one
            sample at a time. Intuitively you may think the rest of guidance
            scales are between 0 and 1, but it is common to use a scale greater
            than 1 as a method of amplifying the prompt's influence on the
            image, pushing it further away from the unconditional sample.

        Returns
        -------
        torch.Tensor
            The generated image in RGB scaled in [0, 1] with tensor shape (H,
            W, 3). The height and the width may depend on the underlying Stable
            Diffusion version, but is typically 512x512.
        """

        # Determine if need dual samples
        do_classifier_free_guidance = guidance_scale != 1.0

        # Encode text prompt
        text_embeddings = self._encode_text_prompt(
            prompt,
            do_classifier_free_guidance=do_classifier_free_guidance,
        )

        # Set up time steps
        self.scheduler.set_timesteps(num_steps)
        timesteps = self.scheduler.timesteps

        # Randomly generate initial noise (latents) based on random seed
        # We generate the random in numpy and not torch to be consistent with
        # the reference implementation.
        num_channels_latents = self.unet.in_channels
        latents_shape = (1, num_channels_latents, self.unet.height, self.unet.width)
        rng = np.random.RandomState(seed)
        latents = rng.normal(
            scale=self.scheduler.init_noise_sigma, size=latents_shape
        ).astype(np.float32)
        latents = torch.from_numpy(latents)

        # Set up progress bar
        tqdm_context = tqdm(
            enumerate(timesteps),
            total=len(timesteps),
            desc="Generating image",
            colour="magenta",
        )

        # Main denoising loop
        for _, t in tqdm_context:
            # For classifier free guidance, make a copy of the latent vector
            latent_model_input = torch.tile(
                latents, (2 if do_classifier_free_guidance else 1, 1, 1, 1)
            )

            # Scale the latent vector based on the current timestep
            latent_model_input = self.scheduler.scale_model_input(latent_model_input, t)

            # Predict the noise residual using the UNet denoiser
            (noise_pred,) = self.unet(
                latent_model_input,
                torch.tensor([t, t], dtype=torch.float32),
                text_embeddings,
            )

            # If using classifier-free guidance, interpolate between the
            # unconditional and conditional samples based on the guidance scale
            if do_classifier_free_guidance:
                noise_pred_uncond, noise_pred_text = torch.split(noise_pred, 1, dim=0)
                noise_pred = noise_pred_uncond + guidance_scale * (
                    noise_pred_text - noise_pred_uncond
                )

            # Denoise the latents based on the noise prediction
            latents = self.scheduler.step(
                noise_pred,
                t,
                latents,
            ).prev_sample

            gc.collect()

        # Rescale latents and decode into RGB image
        latents *= 1 / 0.18215
        image = self.vae_decoder(latents)

        # Rescale image to [0, 1] and permute to (height, width, 3)
        image = torch.clip(image / 2.0 + 0.5, 0, 1)
        image = image.squeeze(0).permute(1, 2, 0)
        return image
