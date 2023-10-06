from tetra_model_zoo.imagenet_classifier.test_utils import run_imagenet_classifier_test
from tetra_model_zoo.resnext101.model import MODEL_ID, ResNeXt101


def test_numerical():
    run_imagenet_classifier_test(
        ResNeXt101.from_pretrained(), MODEL_ID, probability_threshold=0.46
    )
