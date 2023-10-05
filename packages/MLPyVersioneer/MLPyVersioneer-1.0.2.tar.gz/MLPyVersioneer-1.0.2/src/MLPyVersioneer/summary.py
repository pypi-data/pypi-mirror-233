from torch import nn
import keras
from sklearn.base import BaseEstimator
import os
import re

from exporter import Exporter
from training_phase_metric_storage import TrainingPhaseMetricStorage

SUMMARY_FOLDER = "meta_data"

SUMMARY_FOLDER = "meta_data"

class Summary:
    """
    Class to summarize the model details including hyperparameters, architecture, and performance metrics.

    Attributes:
    - model (nn.Module): The PyTorch model to be summarized.
    - model_name (str): A descriptive name for the model.
    - hyperparameters (dict): The model's hyperparameters.
    - performance_metrics (dict): Performance metrics like accuracy, loss, etc.
    - training_phase_metrics_storage (TrainingPhaseMetricStorage): Storage for metrics during training phases.
    - version (int): Model version determined based on existing saved summaries.
    """

    def __init__(self, model, model_name: str = "model", hyperparameters: dict = None, performance_metrics: dict = None) -> None:
        self.model = model
        self.model_name = model_name
        self.hyperparameters = hyperparameters
        self.performance_metrics = performance_metrics
        self.training_phase_metrics_storage = TrainingPhaseMetricStorage()
        self.exporter = Exporter()  # Assumes the Exporter class has methods for generating folders and files.
        self.version = self._determine_next_version()

    def save(self) -> None:
        """
        Save the model summary.
        """
        self.exporter.create_required_folders()
        self.exporter.save_model_summary(self)

    def update_hyperparameters(self, hyperparameters: dict) -> None:
        """
        Update model hyperparameters.

        Args:
        - hyperparameters (dict): Dictionary of hyperparameters.
        """
        self.hyperparameters = hyperparameters

    def update_performance_metrics(self, performance_metrics: dict) -> None:
        """
        Update model performance metrics.

        Args:
        - performance_metrics (dict): Dictionary of performance metrics.
        """
        self.performance_metrics = performance_metrics

    def get_architecture(self) -> dict:
        """
        Retrieve model architecture details.

        Returns:
        - architecture (dict): Dictionary representation of model architecture or None if model is not of type nn.Module.
        """
        # PyTorch
        if isinstance(self.model, nn.Module):  # Assumes PyTorch's nn.Module
            return {str(name): str(value) for name, value in self.model.named_children()}
        
        # Keras
        elif isinstance(self.model, keras.models.Model):
            layers = [(layer.name, layer.get_config()) for layer in self.model.layers]
            return dict(layers)
        
        # Scikit-learn
        elif isinstance(self.model, BaseEstimator):
            return {"class": str(self.model.__class__), "params": self.model.get_params()}
    
        # Other
        else:
            raise TypeError("Model type is not supported.")

    def add_training_phase_metric(self, metrics_dict: dict) -> None:
        """
        Add a TrainingPhaseMetric instance to the storage using a dictionary format.

        Args:
        - metric_dict (dict): Dictionary containing 'name', 'value', and 'epoch' keys.
        """
        self.training_phase_metrics_storage.add_metric_from_dict(metrics_dict)

    def _determine_next_version(self) -> int:
        """
        Determine the next version number for the model based on existing saved summaries.

        Returns:
        - version (int): Next version number for the model.
        """
        try:
            files = os.listdir(SUMMARY_FOLDER)
        except FileNotFoundError:
            return 1

        # Filter files corresponding to the current model name
        relevant_files = [file for file in files if file.split("_")[0] == self.model_name]

        # Extract versions from the filenames
        versions = [int(re.findall(r'\d+', file)[0]) for file in relevant_files]

        if not versions:  # If there are no relevant files, start at version 1
            return 1

        latest_version = max(versions)
        return latest_version + 1