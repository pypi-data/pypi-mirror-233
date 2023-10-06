from tetra_model_zoo.imagenet_classifier.test_utils import run_imagenet_classifier_test
from tetra_model_zoo.regnet.model import MODEL_ID, RegNet


def test_numerical():
    run_imagenet_classifier_test(
        RegNet.from_pretrained(), MODEL_ID, probability_threshold=0.68
    )
