import os
import sys
import torch
import keras
import joblib
from sklearn.base import BaseEstimator
import json
from datetime import datetime

import os
import sys
import json
from datetime import datetime
import torch
import keras
import re

SUMMARY_FOLDER = "meta_data"
MODEL_FOLDER = "models"
ALL_FOLDERS = [SUMMARY_FOLDER, MODEL_FOLDER]

class Exporter:
    """
    Class responsible for generating required folders and saving model details and checkpoints.

    Methods:
    - create_required_folders: Ensure all necessary folders exist or create them.
    - save_model_summary: Save a model's metadata and state to files.
    """

    def create_required_folders(self) -> None:
        """
        Create the required folders if they do not exist.
        """
        try:
            for folder in ALL_FOLDERS:
                os.makedirs(folder, exist_ok=True)
        except Exception as e:
            print(f"Error: Could not create folders. Reason: {e}")
            sys.exit(1)

    def save_model_summary(self, summary) -> None:
        """
        Save the model's metadata as JSON and its state as a PyTorch checkpoint.

        Args:
        - summary (Summary): An instance of the Summary class containing model details.
        """
        summary_data = {
            "timestamp": str(datetime.now()),
            "model_name": summary.model_name,
            "version": summary.version,
            "architecture": summary.get_architecture() or "Not Available",
            "hyperparameters": summary.hyperparameters or {},
            "performance_metrics": summary.performance_metrics or {},
            "training_phase_metrics": summary.training_phase_metrics_storage.get_metrics_as_dicts() or {},
        }

        # Save model metadata as JSON
        summary_file_path = os.path.join(SUMMARY_FOLDER, f"{summary.model_name}_v{summary.version}.json")
        with open(summary_file_path, "w") as f:
            json.dump(summary_data, f, indent=4)

        # Save the model state
        if isinstance(summary.model, torch.nn.Module):
            model_file_path = os.path.join(MODEL_FOLDER, f"{summary.model_name}_v{summary.version}.pt")
            torch.save(summary.model.state_dict(), model_file_path)  # It's recommended to save state_dict instead of the whole model

        elif isinstance(summary.model, keras.Model):
            model_file_path = os.path.join(MODEL_FOLDER, f"{summary.model_name}_v{summary.version}.h5")
            summary.model.save(model_file_path)

        elif isinstance(summary.model, BaseEstimator):
            model_file_path = os.path.join(MODEL_FOLDER, f"{summary.model_name}_v{summary.version}.pkl")
            joblib.dump(summary.model, model_file_path)


