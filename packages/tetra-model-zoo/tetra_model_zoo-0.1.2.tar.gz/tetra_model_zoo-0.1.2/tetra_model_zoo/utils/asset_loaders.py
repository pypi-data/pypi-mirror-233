import os
import sys
import threading
import time
from enum import Enum
from platform import system
from typing import Any, Callable, Optional

import gdown
import requests
import yaml
from git import Repo
from PIL import Image
from schema import And, Schema, SchemaError


class MODEL_ZOO_WEB_ASSET(Enum):
    STATIC_IMG = 0
    ANIMATED_MOV = 1


class ModelZooAssetConfig:
    def __init__(
        self,
        asset_url: str,
        web_asset_folder: str,
        static_web_banner_filename: str,
        animated_web_banner_filename: str,
        model_asset_folder: str,
        local_store_path: str,
    ) -> None:
        self.local_store_path = local_store_path
        self.asset_url = asset_url
        self.web_asset_folder = web_asset_folder
        self.static_web_banner_filename = static_web_banner_filename
        self.animated_web_banner_filename = animated_web_banner_filename
        self.model_asset_folder = model_asset_folder

        # Validation
        for name in [
            self.asset_url,
            self.web_asset_folder,
            self.model_asset_folder,
            self.static_web_banner_filename,
            self.animated_web_banner_filename,
            self.local_store_path,
        ]:
            assert not name.endswith("/") and not name.endswith("\\")
        for name in [
            self.static_web_banner_filename,
            self.animated_web_banner_filename,
        ]:
            assert not name.startswith("/") and not name.startswith("\\")

    def get_web_asset_url(self, model_id: str, type: MODEL_ZOO_WEB_ASSET):
        if type == MODEL_ZOO_WEB_ASSET.STATIC_IMG:
            file = self.static_web_banner_filename
        elif type == MODEL_ZOO_WEB_ASSET.ANIMATED_MOV:
            file = self.animated_web_banner_filename
        else:
            raise NotImplementedError("unsupported web asset type")
        return f"{self.asset_url}/{ModelZooAssetConfig._replace_path_keywords(self.web_asset_folder, model_id)}/{file}"

    def get_local_store_path(self, model_id: str, version: int, file_name: str):
        assert not file_name.startswith("/") and not file_name.startswith("\\")
        if system() == "Windows":
            file_name = file_name.replace("/", "\\")
        return os.path.join(
            self.local_store_path, get_model_asset_s3_path(model_id, version, file_name)
        )

    def get_local_store_model_dir_path(self, model_name: str, create=False) -> str:
        model_dir = os.path.join(self.local_store_path, model_name)
        if create:
            os.makedirs(model_dir, exist_ok=True)
        return model_dir

    def get_model_asset_s3_path(self, model_id: str, version: int, file_name: str):
        assert not file_name.startswith("/") and not file_name.startswith("\\")
        return f"{ModelZooAssetConfig._replace_path_keywords(self.model_asset_folder, model_id, version)}/{file_name}"

    def get_model_asset_url(self, model_id: str, version: int, file_name: str):
        assert not file_name.startswith("/") and not file_name.startswith("\\")
        return (
            f"{self.asset_url}/{get_model_asset_s3_path(model_id, version, file_name)}"
        )

    ###
    # Helpers
    ###
    @staticmethod
    def _replace_path_keywords(
        path: str, model_id: Optional[str] = None, version: Optional[int] = None
    ):
        if model_id:
            path = path.replace("{model_id}", model_id)
        if version:
            path = path.replace("{version}", str(version))
        return path

    ###
    # Load from CFG
    ###
    @staticmethod
    def from_cfg(
        asset_cfg_path: str = os.path.join(
            os.path.dirname(__file__), "asset_bases.yaml"
        ),
        local_store_path: str = os.path.join(
            os.path.expanduser("~"), ".tetra", "model-zoo"
        ),
    ):
        # Load CFG and params
        asset_cfg = ModelZooAssetConfig.load_asset_cfg(asset_cfg_path)
        return ModelZooAssetConfig(
            asset_cfg["store_url"],
            asset_cfg["web_asset_folder"],
            asset_cfg["static_web_banner_filename"],
            asset_cfg["animated_web_banner_filename"],
            asset_cfg["model_asset_folder"],
            local_store_path,
        )

    ASSET_CFG_SCHEMA = Schema(
        {
            "store_url": And(str),
            "web_asset_folder": And(str),
            "static_web_banner_filename": And(str),
            "animated_web_banner_filename": And(str),
            "model_asset_folder": And(str),
        }
    )

    @staticmethod
    def load_asset_cfg(path):
        with open(path) as f:
            data = yaml.safe_load(f)
            try:
                # Validate high level-schema
                ModelZooAssetConfig.ASSET_CFG_SCHEMA.validate(data)
            except SchemaError as e:
                assert 0, f"{e.code} in {path}"
            return data


ASSET_CONFIG = ModelZooAssetConfig.from_cfg()


def get_web_asset_url(model_id: str, type: MODEL_ZOO_WEB_ASSET):
    return ASSET_CONFIG.get_web_asset_url(model_id, type)


def get_model_asset_url(model_id: str, version: int, file_name: str):
    return ASSET_CONFIG.get_model_asset_url(model_id, version, file_name)


def get_local_store_path(model_id: str, version: int, file_name: str):
    return ASSET_CONFIG.get_local_store_path(model_id, version, file_name)


def get_model_asset_s3_path(model_id: str, version: int, file_name: str):
    return ASSET_CONFIG.get_model_asset_s3_path(model_id, version, file_name)


def _query_yes_no(question, default="yes"):
    """
    Ask a yes/no question and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".

    Sourced from https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        print(question + prompt, end="")
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def maybe_clone_git_repo(git_file_path: str, commit_hash, model_name: str) -> str:
    """Clone (or pull) a repository, save it to disk in a standard location,
    and return the absolute path to the cloned location."""

    # http://blah.come/author/name.git -> name, author
    repo_name = os.path.basename(git_file_path).split(".")[0]
    repo_author = os.path.basename(os.path.dirname(git_file_path))
    local_path = os.path.join(
        ASSET_CONFIG.get_local_store_model_dir_path(model_name, True),
        f"{repo_author}_{repo_name}_git",
    )

    if not os.path.exists(os.path.join(local_path, ".git")):
        # Clone repo
        should_clone = _query_yes_no(
            f"{model_name} requires repository {git_file_path} . Ok to clone?",
        )
        if should_clone:
            print(f"Cloning {git_file_path}to {local_path}...")
            repo = Repo.clone_from(git_file_path, local_path)
            repo.git.checkout(commit_hash)
            print("Done")
        else:
            raise ValueError(
                f"Unable to load {model_name} without its required repository."
            )

    return local_path


class SourceAsRoot:
    THREAD_LOCK = threading.Lock()

    """
    Context manager that runs code with:
     * the source repository added to the system path,
     * cwd set to the source repo's root directory.

    Only one of this class should be active per Python session.
    """

    def __init__(
        self,
        source_repo_url: str,
        source_repo_commit_hash: str,
        source_repo_name: str,
    ):
        self.source_repo_url = source_repo_url
        self.source_repo_commit_hash = source_repo_commit_hash
        self.source_repo_name = source_repo_name

    def __enter__(self):
        SourceAsRoot.THREAD_LOCK.acquire()
        self.repository_path = maybe_clone_git_repo(
            self.source_repo_url, self.source_repo_commit_hash, self.source_repo_name
        )
        self.cwd = os.getcwd()

        # Patch path for this load only, since the model source
        # code references modules via a global scope.
        sys.path.append(self.repository_path)
        os.chdir(self.repository_path)

    def __exit__(self, exc_type, exc_value, exc_tb):
        # Reset global state
        os.chdir(self.cwd)
        sys.path.remove(self.repository_path)
        SourceAsRoot.THREAD_LOCK.release()


def download_model_asset(model_id: str, version: int, file_name: str) -> str:
    """
    Parameters:
    - model_id: Model ID
    - version: Asset version
    - file_name: file name of asset

    Returns:
    - The local filepath of the download data.
    """
    return download_data(get_model_asset_url(model_id, version, file_name), model_id)


def download_model_image_asset(
    model_id: str, version: int, file_name: str
) -> Image.Image:
    """
    Parameters:
    - model_id: Model ID
    - version: Asset version
    - file_name: file name of asset

    Returns:
    - Opened image
    """
    return Image.open(download_model_asset(model_id, version, file_name))


def download_data(url: str, model_name: str) -> str:
    """
    Downloads data from the internet and stores it in the same directory as
    other assets for the model. Returns the local filepath of the downloaded data.
    """
    dst_path = os.path.join(
        ASSET_CONFIG.get_local_store_model_dir_path(model_name, True),
        url.rsplit("/", 1)[-1],
    )
    if not os.path.exists(dst_path):
        print(f"Downloading data at {url} to {dst_path}... ", end="")
        file_data = requests.get(url)
        if file_data.status_code != 200:
            raise ValueError(f"Unable to download file at {url}")
        with open(dst_path, "wb") as dst_file:
            dst_file.write(file_data.content)
        print("Done")
    return dst_path


def download_google_drive(file_id: str, model_name: str, filename: str):
    """
    Download file from google drive to the local directory.

    Parameters:
        file_id: Unique identifier of the file in Google Drive.
            Typically found in the URL.
        model_name: Model for which this asset is being downloaded.
            Used to choose where in the local filesystem to put it.
        filename: Filename under which it will be saved locally.

    Returns:
        Filepath within the local filesystem.
    """
    dst_path = os.path.join(
        ASSET_CONFIG.get_local_store_model_dir_path(model_name, True), filename
    )
    if not os.path.exists(dst_path):
        url = f"https://drive.google.com/uc?id={file_id}"
        print(f"Downloading data at {url} to {dst_path}... ", end="")
        gdown.download(url, dst_path, quiet=False)
        print("Done")
    return dst_path


def load_image(image_path: str, model_name: str) -> Image.Image:
    """Loads an image from the specified path.
    Will first download the image to the appropriate standard location if image_path is a URL."""
    if image_path.startswith("http"):
        image_path = download_data(image_path, model_name)

    return Image.open(image_path)


def callback_with_retry(
    num_retries: int,
    callback: Callable,
    *args: Optional[Any],
    **kwargs: Optional[Any],
) -> Any:
    """Allow retries when running provided function."""
    if num_retries == 0:
        raise RuntimeError(f"Unable to run function {callback.__name__}")
    else:
        try:
            return callback(*args, **kwargs)
        except Exception as error:
            error_msg = (
                f"Error: {error.message}"
                if hasattr(error, "message")
                else f"Error: {str(error)}"
            )
            print(error_msg)
            if hasattr(error, "status_code"):
                print(f"Status code: {error.status_code}")
            time.sleep(10)
            return callback_with_retry(num_retries - 1, callback, *args, **kwargs)
