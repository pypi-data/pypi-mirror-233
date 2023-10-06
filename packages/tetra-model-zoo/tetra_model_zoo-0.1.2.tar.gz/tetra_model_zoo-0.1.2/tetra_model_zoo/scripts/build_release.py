import os
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

from tetra_model_zoo.scripts.generate_summary import generate_table
from tetra_model_zoo.utils.config_loaders import (
    MODEL_ZOO_STATUS,
    ZOO_MODEL_IDS,
    ZOO_REPO_DIR,
    ModelZooModelInfo,
    get_zoo_model_package,
)

ZOO_MODELS: List[ModelZooModelInfo] = [
    ModelZooModelInfo.from_model(id) for id in ZOO_MODEL_IDS
]

PRIVATE_MODELS = [cfg for cfg in ZOO_MODELS if cfg.status == MODEL_ZOO_STATUS.PRIVATE]
PUBLIC_MODELS = [cfg for cfg in ZOO_MODELS if cfg.status == MODEL_ZOO_STATUS.PUBLIC]

# Output folder
OUTPUT_FOLDER = TemporaryDirectory()

# Copy repo root
OUTPUT_ROOT = Path(OUTPUT_FOLDER.name) / "model-zoo"
shutil.copytree(ZOO_REPO_DIR, OUTPUT_ROOT)
ZOO_MODEL_PACKAGE = get_zoo_model_package(OUTPUT_ROOT)

# Remove private models
for model in PRIVATE_MODELS:
    shutil.rmtree(ZOO_MODEL_PACKAGE / model.id)

# Remove private yamls
for model in PUBLIC_MODELS:
    os.remove(ZOO_MODEL_PACKAGE / model.id / "info.yaml")
    os.remove(ZOO_MODEL_PACKAGE / model.id / "perf.yaml")

# Remove private tests
os.remove(ZOO_MODEL_PACKAGE / "utils" / "config_loaders.py")
os.remove(ZOO_MODEL_PACKAGE / "utils" / "test_info_specs.py")

# Dump README Table
updated_readme = generate_table(PUBLIC_MODELS)

# Remove Private Models from ReadMe
README_PATH = OUTPUT_ROOT / "README.md"
readme_text = []
with open(README_PATH, "a") as global_readme:
    global_readme.write(updated_readme)

# Copy model zoo to downloads
shutil.move(OUTPUT_ROOT, "/Users/kory/Downloads/model-zoo")
