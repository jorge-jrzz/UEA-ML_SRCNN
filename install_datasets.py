import os
import shutil
from pathlib import Path
from typing import Literal

import kagglehub


__all__ = ["download_datasets"]


def is_colab():
    try:
        import google.colab
        return True
    except ImportError:
        return False

def delete_donwload_cache(download_path: str, dataset: Literal["Set5", "DIV2K"]) -> None:
    """
    Delete the cache donwload directory.
    """
    delete_dir = Path(download_path)
    count = 1
    while count <= len(delete_dir.parts):
        delete_dir = delete_dir.parent
        count += 1
        if dataset == "Set5" and delete_dir.name == "ll01dm":
            print("Deleting cache directory for Set5 download")
            shutil.rmtree(delete_dir)
            break
        elif dataset == "DIV2K" and delete_dir.name == "joe1995":
            print("Deleting cache directory for DIV2K download")
            shutil.rmtree(delete_dir)
            break

def download_dataset(dataset: Literal["Set5", "DIV2K"]) -> None:
    """
    Download a dataset from Kaggle.
    """
    if dataset != "Set5" and dataset!= "DIV2K":
        raise ValueError("dataset must be 'Set5' or 'DIV2K'")
    print(f"📥 Descargando dataset: {dataset}...")
    download_path = None
    if dataset == "Set5":
        download_path = kagglehub.dataset_download("ll01dm/set-5-14-super-resolution-dataset", force_download=True)
        dataset_paths = Path(download_path) / dataset / dataset
        dst_path = Path(os.getcwd()) / dataset
        shutil.copytree(dataset_paths, dst_path, dirs_exist_ok=True)
    elif dataset == "DIV2K":
        download_path = kagglehub.dataset_download("joe1995/div2k-dataset", force_download=True)
        for subdir in ["DIV2K_train_HR", "DIV2K_valid_HR"]:
            dataset_path = Path(download_path) / subdir / subdir
            dst_path = Path(os.getcwd()) / dataset / subdir
            shutil.copytree(dataset_path, dst_path, dirs_exist_ok=True)
    if not is_colab():
      delete_donwload_cache(download_path, dataset)

def download_datasets():
  download_dataset("Set5")
  download_dataset("DIV2K")
