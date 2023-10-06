import os
from pathlib import Path

import numpy as np
import pytest
import torch
import whisper

from tetra_model_zoo.utils.asset_loaders import download_data, get_model_asset_url
from tetra_model_zoo.whisper_asr.app import WhisperApp, load_audio, load_mel_filter
from tetra_model_zoo.whisper_asr.model import (
    MEL_FILTER_PATH,
    MODEL_ASSET_VERSION,
    MODEL_ID,
    Whisper,
    WhisperDecoderInf,
    WhisperEncoderInf,
)

APP_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TEST_AUDIO_PATH = get_model_asset_url(MODEL_ID, MODEL_ASSET_VERSION, "audio/jfk.npz")


@pytest.fixture(scope="session")
def mel_input() -> np.ndarray:
    mel_filter_path = download_data(MEL_FILTER_PATH, MODEL_ID)
    mel_filter = load_mel_filter(mel_filter_path)
    audio_path = download_data(TEST_AUDIO_PATH, MODEL_ID)
    return load_audio(mel_filter, audio_path)


def test_numerics(mel_input):
    """
    Test that wrapper classes predict logits (without post processing) that
    matches with the original model's.
    """
    # OpenAI
    with torch.no_grad():
        mel_input = torch.from_numpy(mel_input)
        model = whisper.load_model("tiny.en")
        audio_features = model.encoder(mel_input)

        tokens = torch.LongTensor([[50257]])
        logits_orig = model.decoder(tokens, audio_features).detach().numpy()

    # Tetra
    encoder = WhisperEncoderInf(model)
    decoder = WhisperDecoderInf(model.decoder)

    cross_attn_cache = encoder(mel_input)
    cache_tensor = np.array([], dtype=np.float32).reshape((1, 0, 384))
    self_attn_cache = [torch.from_numpy(cache_tensor)] * 2 * 4

    decoder_out = decoder(tokens, *cross_attn_cache, *self_attn_cache)
    logits = decoder_out[0].detach().numpy()

    np.testing.assert_allclose(logits_orig, logits)


def test_transcribe(mel_input):
    """
    Test that pytorch wrappers produces end to end transcription results that
    matches with the original model
    """
    # Run inference with OpenAI whisper
    with torch.no_grad():
        model = whisper.load_model("tiny.en")
        options = whisper.DecodingOptions(
            language="en", without_timestamps=False, fp16=False
        )
        results = model.decode(torch.from_numpy(mel_input).float(), options)
        text_orig = results[0].text

    app = WhisperApp(Whisper.from_source_model(model))

    # Perform transcription
    transcription = app.transcribe(mel_input)
    assert transcription == text_orig
