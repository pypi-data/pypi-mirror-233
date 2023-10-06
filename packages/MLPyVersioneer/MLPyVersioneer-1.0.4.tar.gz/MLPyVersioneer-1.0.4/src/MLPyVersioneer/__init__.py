import logging

# Suppress logs for specific library or globally
#logging.getLogger("tensorflow").setLevel(logging.CRITICAL)
# OR for global suppression:
logging.getLogger().setLevel(logging.CRITICAL)


from .summary import Summary
from .training_phase_metric_storage import TrainingPhaseMetricStorage
