import kaggle

import os
import kaggle

def download_kaggle_dataset(dataset: str, save_path: str):
    """
    Downloads a Kaggle dataset and extracts it.
    
    Parameters:
        dataset (str): The dataset identifier in 'owner/dataset-name' format.
        save_path (str): The path where the dataset should be saved.
    """
    os.makedirs(save_path, exist_ok=True)
    
    print(f"Downloading dataset: {dataset}...")
    
    kaggle.api.dataset_download_files(dataset, path=save_path, unzip=True)
    
    print(f"Dataset downloaded and extracted to {save_path}")

# # Example usage
# if __name__ == "__main__":
#     dataset_name = "zynicide/wine-reviews"  # Replace with the actual dataset
#     save_directory = "/workspaces/disent-data-science/Data_nerd/Data_science/Get the data 1"
    
#     download_kaggle_dataset(dataset_name, save_directory)
