from typing import List

from tetra_model_zoo.utils.config_loaders import (
    MODEL_ZOO_DOMAIN,
    MODEL_ZOO_USE_CASE,
    ModelZooModelInfo,
)

TABLE_TITLE = (
    "| Model | README | Torch App | Device Export | CLI Demo\n| -- | -- | -- | -- | --"
)
TABLE_DIVIDER = "| | | | |"
subdomains = {
    MODEL_ZOO_DOMAIN.COMPUTER_VISION: [
        MODEL_ZOO_USE_CASE.IMAGE_CLASSIFICATION,
        MODEL_ZOO_USE_CASE.IMAGE_EDITING,
        MODEL_ZOO_USE_CASE.SUPER_RESOLUTION,
        MODEL_ZOO_USE_CASE.SEGMENTATION,
        MODEL_ZOO_USE_CASE.SEMANTIC_SEGMENTATION,
        MODEL_ZOO_USE_CASE.VIDEO_CLASSIFICATION,
        MODEL_ZOO_USE_CASE.OBJECT_DETECTION,
        MODEL_ZOO_USE_CASE.POSE_ESTIMATION,
        MODEL_ZOO_USE_CASE.IMAGE_TO_TEXT,
    ],
    MODEL_ZOO_DOMAIN.AUDIO: [MODEL_ZOO_USE_CASE.SPEECH_RECOGNITION],
    MODEL_ZOO_DOMAIN.MULTIMODAL: [],  # Anything is OK
}


def get_title_divider(title: str):
    return f"{TABLE_DIVIDER}\n| **{title}**"


def get_model_entry(model: ModelZooModelInfo):
    return f"| [{model.name}](https://tetra.ai/model-zoo/{model.id}) | [tetra_model_zoo.{model.id}](tetra_model_zoo/{model.id}/README.md) | ✔️ | ✔️ | ✔️"


def generate_table(models: List[ModelZooModelInfo]):
    out = ""
    for domain in MODEL_ZOO_DOMAIN:
        domain_models = [
            model_cfg for model_cfg in models if model_cfg.domain == domain
        ]
        if not domain_models:
            continue

        out = f"""{out}\

### {domain.to_string()}

{TABLE_TITLE}
"""

        use_cases = subdomains[domain]
        if not use_cases:
            # Dump everything into 1 table
            out = f"{out}{TABLE_DIVIDER}\n"
            for model in domain_models:
                out = out + get_model_entry(model) + "\n"
        else:
            for use_case in use_cases:
                use_case_models = [
                    model for model in domain_models if model.use_case == use_case
                ]
                if not use_case_models:
                    continue
                out = f"{out}{get_title_divider(use_case.to_string())}\n"
                for model in use_case_models:
                    out = f"{out}{get_model_entry(model)}\n"

    return out
