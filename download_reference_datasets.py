import os
import zipfile
import subprocess

def download_and_extract_kaggle(dataset, dest_folder):
    """
    Download and extract a Kaggle dataset using the Kaggle API.
    dataset: str, e.g. 'shrutisaxena/yoga-pose-image-classification-dataset'
    dest_folder: str, where to extract
    """
    os.makedirs(dest_folder, exist_ok=True)
    zip_path = os.path.join(dest_folder, dataset.split('/')[-1] + '.zip')
    print(f"Downloading {dataset} to {zip_path} ...")
    subprocess.run(["kaggle", "datasets", "download", "-d", dataset, "-p", dest_folder, "--unzip"], check=True)
    print(f"Extracted to {dest_folder}")

if __name__ == "__main__":
    datasets = [
        "shrutisaxena/yoga-pose-image-classification-dataset",
        "tr1gg3rtrash/yoga-posture-dataset",
        # Mendeley dataset is not on Kaggle, download manually if needed
    ]
    dest = os.path.join("static", "reference_poses")
    for ds in datasets:
        download_and_extract_kaggle(ds, dest)
    print("All datasets downloaded and extracted.")
