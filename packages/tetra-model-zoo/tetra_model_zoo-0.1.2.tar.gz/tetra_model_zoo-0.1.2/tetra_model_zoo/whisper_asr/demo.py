import whisper

from tetra_model_zoo.utils.asset_loaders import download_data
from tetra_model_zoo.whisper_asr.app import WhisperApp, load_audio, load_mel_filter
from tetra_model_zoo.whisper_asr.model import MEL_FILTER_PATH, MODEL_ID, Whisper
from tetra_model_zoo.whisper_asr.test import TEST_AUDIO_PATH

if __name__ == "__main__":
    # For other model sizes, see https://github.com/openai/whisper/blob/main/whisper/__init__.py#L17
    model = whisper.load_model("tiny.en")
    app = WhisperApp(Whisper.from_pretrained())

    # Load audio into mel spectrogram
    mel_filter_path = download_data(MEL_FILTER_PATH, MODEL_ID)
    mel_filter = load_mel_filter(mel_filter_path)

    audio_path = download_data(TEST_AUDIO_PATH, MODEL_ID)
    mel_input = load_audio(mel_filter, audio_path)

    # Perform transcription
    transcription = app.transcribe(mel_input)
    print("Transcription:", transcription)
