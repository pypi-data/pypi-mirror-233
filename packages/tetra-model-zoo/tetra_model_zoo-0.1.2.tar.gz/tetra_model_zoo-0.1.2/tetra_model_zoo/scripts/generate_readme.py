import os
from pathlib import Path

ZOO_MODEL_PACKAGE = Path(__file__).parent / "tetra_model_zoo"
ZOO_MODEL_DIRS = [
    Path(f.path)
    for f in os.scandir(ZOO_MODEL_PACKAGE)
    if f.is_dir() and "info.yaml" in os.listdir(f)
]

PACKAGE_INSTALL_INSTRUCTIONS = """
Install the package via pip:
```
pip install tetra_model_zoo[trocr]
```

"""


def main():
    for folder in ZOO_MODEL_DIRS:
        # needs_install_instructions = "requirements.txt" in os.listdir(folder)
        # model_id = folder.name

        readme_path = folder / "README.md"
        if os.path.exists(readme_path):
            os.remove(readme_path)


if __name__ == "main":
    main()
