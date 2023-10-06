import torch

from tetra_model_zoo.imagenet_classifier.model import DocstringInheritorMeta


class KineticsClassifier(torch.nn.Module, metaclass=DocstringInheritorMeta):
    """
    Base class for all Kinetics Classifier models within the model zoo.
    """

    def __init__(self, net: torch.nn.Module):
        """
        Basic initializer which takes in a pretrained classifier network.
        Subclasses can choose to implement their own __init__ and forward methods.
        """
        super().__init__()
        self.net = net

    def forward(self, video: torch.Tensor):
        """
        Predict class probabilities for an input `video`.

        Parameters:
            video: A [C, Number of frames, H, W] video.
                   Assumes video has been resized and normalized as implemented
                   in the preprocess_image function in video_preprocessing.py file.
                   Pixel values pre-processed for encoder consumption.
                   Range: float[0, 1]
                   3-channel Color Space: RGB

        Returns:
            A [1, 400] where each value is the log-likelihood of
            the video belonging to the corresponding Kinetics class.
        """
        return self.net(video)
