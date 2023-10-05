from training_phase_metric import TrainingPhaseMetric
import csv
import json
import pandas as pd
import plotly.graph_objs as go


class TrainingPhaseMetricStorage():
    """
    Class to store and manage TrainingPhaseMetric instances.
    Metrics are grouped by their names.
    """
    
    def __init__(self) -> None:
        self.storage = {}

    @staticmethod
    def load_from_json(json_path: str):
        """
        Load TrainingPhaseMetrics from a JSON file and return a populated TrainingPhaseMetricStorage instance.

        Args:
        - json_path (str): Path to the JSON file.

        Returns:
        - TrainingPhaseMetricStorage: A populated storage instance.
        """
        storage = TrainingPhaseMetricStorage()

        with open(json_path, 'r') as file:
            metrics_list = json.load(file)["training_phase_metrics"]


        for metric_data in metrics_list:
            metric = TrainingPhaseMetric(
                metric_data['name'],
                metric_data['value'],
                metric_data['epoch']
            )
            storage.add_metric(metric)
        
        return storage

    def add_metric(self, metric: TrainingPhaseMetric) -> None:
        """
        Add a TrainingPhaseMetric instance to the storage.
        
        Args:
        - metric (TrainingPhaseMetric): The metric to be added.
        """
        if metric.name not in self.storage:
            self.storage[metric.name] = []
        self.storage[metric.name].append(metric)

    def add_metrics_from_dict(self, metrics_dict: dict) -> None:
        """
        Add multiple TrainingPhaseMetric instances to the storage using a dictionary format.

        Args:
        - metrics_dict (dict): Dictionary containing 'epoch' key and then one or more metric names as keys with their corresponding values.
        Example format: {"epoch": 1, "metric1": 0.9, "metric2": 0.4}
        """
        epoch = metrics_dict.get('epoch')
        if epoch is None:
            raise ValueError("The provided dictionary must contain an 'epoch' key.")

        for name, value in metrics_dict.items():
            if name != 'epoch':
                metric = TrainingPhaseMetric(name, value, epoch)
                self.add_metric(metric)

    def get_metrics(self, metric_name: str = None) -> list:
        """
        Get a list of TrainingPhaseMetric instances for a given metric name.
        If no name is provided, returns all metrics.
        
        Args:
        - metric_name (str, optional): The name of the metric.

        Returns:
        - List of TrainingPhaseMetric instances.
        """
        if metric_name:
            return self.storage.get(metric_name, [])
        else:
            return [metric for metrics in self.storage.values() for metric in metrics]

    def get_metrics_as_dicts(self, metric_name: str = None) -> list:
        """
        Get a list of TrainingPhaseMetric instances in dictionary format for a given metric name.
        If no name is provided, returns all metrics in dictionary format.

        Args:
        - metric_name (str, optional): The name of the metric.

        Returns:
        - List of dictionaries representing TrainingPhaseMetric instances.
        """
        metrics = self.get_metrics(metric_name)
        return [metric.__json__() for metric in metrics]

    def __str__(self):
        return "\n".join([f"Metric: {name}\n" + "\n".join(map(str, metrics)) for name, metrics in self.storage.items()])

    def to_csv(self, csv_path: str) -> None:
        """
        Export the stored TrainingPhaseMetrics to a CSV file.

        Args:
        - csv_path (str): Path to save the CSV file.
        """
        with open(csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Epoch', 'Metric Name', 'Value'])  # Header

            for metric in self.get_metrics():
                writer.writerow([metric.epoch, metric.name, metric.value])

    def to_json(self, json_path: str) -> None:
        """
        Export the stored TrainingPhaseMetrics to a JSON file.

        Args:
        - json_path (str): Path to save the JSON file.
        """
        with open(json_path, 'w') as file:
            json.dump(self.__json__(), file, indent=4)

    def to_df(self) -> pd.DataFrame:
        """
        Export the stored TrainingPhaseMetrics to a pandas DataFrame.

        Returns:
        - pandas.DataFrame: DataFrame containing the stored metrics.
        """
        return pd.DataFrame([metric.__json__() for metric in self.get_metrics()])
    
    def plot_metric(self, metric_name: str, show : bool = False) -> go.Figure:
        """Plot a metric using Plotly."""
        if metric_name not in self.storage:
            print(f"No metrics found with name: {metric_name}")
            return
        
        metrics = self.get_metrics(metric_name)
        epochs = [metric.epoch for metric in metrics]
        values = [metric.value for metric in metrics]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=epochs, y=values, mode='lines+markers', name=metric_name))
        fig.update_layout(title=f'{metric_name} over Epochs', xaxis_title='Epoch', yaxis_title=metric_name)
        if show:
            fig.show()
        return fig