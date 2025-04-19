import os
import shutil
from pathlib import Path

import kagglehub


__all__ = ["download_dataset"]


def is_colab():
    try:
        import google.colab
        return True
    except ImportError:
        return False

def delete_donwload_cache(download_path: str, dataset_owner: str) -> None:
    """
    Delete the cache donwload directory.
    """
    delete_dir = Path(download_path)
    count = 1
    while count <= len(delete_dir.parts):
        delete_dir = delete_dir.parent
        count += 1
        if delete_dir.name == dataset_owner:
            print("Deleting original download directory for dataset")
            shutil.rmtree(delete_dir)
            break

def download_dataset(dataset: str) -> None:
    """
    Download a dataset from Kaggle.
    """
    dataset_owner = dataset.split("/", 1)[0]
    dataset_name = dataset.split("/", 1)[1]
    print(f"📥 Descargando dataset: {dataset_name} ...")
    download_path = kagglehub.dataset_download(dataset, force_download=True)
    dst_path = Path(os.getcwd()) / dataset
    shutil.copytree(download_path, dst_path, dirs_exist_ok=True)
    if not is_colab():
      delete_donwload_cache(download_path, dataset_owner)
